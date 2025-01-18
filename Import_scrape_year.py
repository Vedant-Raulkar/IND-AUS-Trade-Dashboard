import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment to run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # Navigate to the website
    driver.get("https://tradestat.commerce.gov.in/eidb/default.asp")

    # Wait for the page to load and click on the specific link
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/table[1]/tbody/tr[7]/td[6]/p/a"))
    ).click()

    # Wait for the first dropdown menu to load
    year_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='select2']")) 
    )

    # Get all available years
    years = [option.get_attribute("value") for option in Select(year_dropdown).options if option.get_attribute("value")]

    # Initialize a DataFrame to store the extracted data
    all_data = pd.DataFrame()

    # Loop through each year
    for year in years:
        Select(year_dropdown).select_by_value(year)
        time.sleep(1)  # Allow time for the second dropdown to update

        # Select "Australia" in the second dropdown
        country_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='select3']")) 
        )
        Select(country_dropdown).select_by_value("17")  # Assuming "17" corresponds to Australia

        # Select the second option in the third dropdown
        commodity_dropdown = driver.find_element(By.XPATH, "//*[@id='select1']")
        Select(commodity_dropdown).select_by_index(1)  # Index 2 (2nd option)

        # Click on the radio buttons
        driver.find_element(By.XPATH, "//*[@id='radioDAll']").click()
        driver.find_element(By.XPATH, "//*[@id='radiousd']").click()

        # Click on the submit button
        driver.find_element(By.XPATH, "//*[@id='button1']").click()

        # Wait for the table to load
        try:
            table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/div/table/tbody"))
            )
            rows = table.find_elements(By.TAG_NAME, "tr")

            # Extract table headers and data
            data = []
            for i, row in enumerate(rows):
                cols = row.find_elements(By.TAG_NAME, "th" if i == 0 else "td")
                data.append([col.text.strip() for col in cols])

            # Convert the data to a DataFrame
            if data:
                df = pd.DataFrame(data[1:], columns=data[0])  # Skip headers
                df["Year"] = year  # Add the year column
                all_data = pd.concat([all_data, df], ignore_index=True)
            else:
                print(f"No data found for the year {year}.")

        except Exception as e:
            print(f"Error extracting table for the year {year}: {e}")

        # Go back to the main page for the next iteration
        driver.back()
        time.sleep(2)

        # Reinitialize dropdowns
        year_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='select2']"))
        )

    # Save the data to an Excel file
    all_data.to_excel("Import_trade_data.xlsx", index=False)
    print("Data extraction complete. Saved to trade_data.xlsx.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the driver
    driver.quit()

import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go

# Load and clean the data
export_file_path = "cleaned_Export_trade_data.xlsx"  # Path for export data
import_file_path = "cleaned_Import_trade_data.xlsx"  # Path for import data

# Load the export trade data
export_data = pd.ExcelFile(export_file_path).parse("Sheet1")
export_data.rename(columns={"Trade Value (USD)": "Trade_Value"}, inplace=True)
export_data_long = export_data.copy()
export_data_long = export_data_long[export_data_long["Trade_Value"].notna()]
export_data_long["Trade_Value"] = export_data_long["Trade_Value"].astype(float)

# Load the import trade data
import_data = pd.ExcelFile(import_file_path).parse("Sheet1")
import_data.rename(columns={"Trade Value (USD)": "Trade_Value"}, inplace=True)
import_data_long = import_data.copy()
import_data_long = import_data_long[import_data_long["Trade_Value"].notna()]
import_data_long["Trade_Value"] = import_data_long["Trade_Value"].astype(float)

# Filter data for "Total"
export_total = export_data_long[export_data_long["Commodity"] == "Total"]
import_total = import_data_long[import_data_long["Commodity"] == "Total"]

# Remove "Total" from the main datasets for bar charts
export_data_long = export_data_long[export_data_long["Commodity"] != "Total"]
import_data_long = import_data_long[import_data_long["Commodity"] != "Total"]

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout for the dashboard
app.layout = html.Div(
    style={"backgroundColor": "#1f1f1f", "color": "#FFFFFF", "padding": "20px"},
    children=[
        html.H1("India-Australia Trade Data Visualization", style={"textAlign": "center"}),

        # Updated layout for vertical stack (column layout)
        html.Div(
            style={"display": "flex", "flexDirection": "column", "alignItems": "center"},
            children=[
                # Export Data Visualization
                html.Div(
                    style={"width": "80%", "marginBottom": "30px"},
                    children=[
                        html.H2("Export Trade Data", style={"textAlign": "center"}),
                        dcc.Dropdown(
                            id="export-commodity-dropdown",
                            options=[
                                {"label": c, "value": c} for c in export_data_long["Commodity"].unique()
                            ],
                            placeholder="Select a Commodity",
                            style={"color": "#000000"},
                        ),
                        dcc.Dropdown(
                            id="export-year-dropdown",
                            options=[
                                {"label": y, "value": y} for y in sorted(export_data["Year"].unique())
                            ],
                            placeholder="Select a Year",
                            style={"color": "#000000"},
                        ),
                        dcc.Graph(id="export-graph"),
                    ],
                ),

                # Import Data Visualization
                html.Div(
                    style={"width": "80%"},
                    children=[
                        html.H2("Import Trade Data", style={"textAlign": "center"}),
                        dcc.Dropdown(
                            id="import-commodity-dropdown",
                            options=[
                                {"label": c, "value": c} for c in import_data_long["Commodity"].unique()
                            ],
                            placeholder="Select a Commodity",
                            style={"color": "#000000"},
                        ),
                        dcc.Dropdown(
                            id="import-year-dropdown",
                            options=[
                                {"label": y, "value": y} for y in sorted(import_data["Year"].unique())
                            ],
                            placeholder="Select a Year",
                            style={"color": "#000000"},
                        ),
                        dcc.Graph(id="import-graph"),
                    ],
                ),
            ],
        ),
    ],
)

# Callback for updating the export graph
@app.callback(
    Output("export-graph", "figure"),
    [Input("export-commodity-dropdown", "value"),
     Input("export-year-dropdown", "value")],
)
def update_export_graph(selected_commodity, selected_year):
    if not selected_commodity and not selected_year:
        return {
            "data": [
                go.Scatter(
                    x=export_total["Year"],
                    y=export_total["Trade_Value"],
                    mode="lines+markers",
                    line=dict(color="cyan"),
                    marker=dict(size=8),
                )
            ],
            "layout": go.Layout(
                title="Total Export Trade Value Over Years",
                xaxis={"title": "Year"},
                yaxis={"title": "Values in US$ Million"},
                plot_bgcolor="#1f1f1f",
                paper_bgcolor="#1f1f1f",
                font=dict(color="white"),
            ),
        }

    filtered_data = export_data_long.copy()

    if selected_commodity and not selected_year:
        filtered_data = filtered_data[filtered_data["Commodity"] == selected_commodity]
        return {
            "data": [
                go.Scatter(
                    x=filtered_data["Year"],
                    y=filtered_data["Trade_Value"],
                    mode="lines+markers",
                    line=dict(color="cyan"),
                    marker=dict(size=8),
                )
            ],
            "layout": go.Layout(
                title=f"Export Trade Data for {selected_commodity}",
                xaxis={"title": "Year"},
                yaxis={"title": "Values in US$ Million"},
                yaxis_range=[0, filtered_data["Trade_Value"].max() * 1.1],
                plot_bgcolor="#1f1f1f",
                paper_bgcolor="#1f1f1f",
                font=dict(color="white"),
            ),
        }

    if selected_year and not selected_commodity:
        filtered_data = filtered_data[filtered_data["Year"] == selected_year]
        return {
            "data": [
                go.Bar(
                    x=filtered_data["Commodity"],
                    y=filtered_data["Trade_Value"],
                    marker=dict(color="cyan"),
                )
            ],
            "layout": go.Layout(
                title=f"Export Trade Data for {selected_year}",
                xaxis={"title": "Commodity"},
                yaxis={"title": "Values in US$ Million"},
                plot_bgcolor="#1f1f1f",
                paper_bgcolor="#1f1f1f",
                font=dict(color="white"),
            ),
        }

    return {
        "data": [],
        "layout": go.Layout(
            title="Select a Commodity or Year to Display Data",
            xaxis={"title": "Year or Commodity"},
            yaxis={"title": "Values in US$ Million"},
            plot_bgcolor="#1f1f1f",
            paper_bgcolor="#1f1f1f",
            font=dict(color="white"),
        ),
    }

# Callback for updating the import graph
@app.callback(
    Output("import-graph", "figure"),
    [Input("import-commodity-dropdown", "value"),
     Input("import-year-dropdown", "value")],
)
def update_import_graph(selected_commodity, selected_year):
    if not selected_commodity and not selected_year:
        return {
            "data": [
                go.Scatter(
                    x=import_total["Year"],
                    y=import_total["Trade_Value"],
                    mode="lines+markers",
                    line=dict(color="yellow"),
                    marker=dict(size=8),
                )
            ],
            "layout": go.Layout(
                title="Total Import Trade Value Over Years",
                xaxis={"title": "Year"},
                yaxis={"title": "Values in US$ Million"},
                plot_bgcolor="#1f1f1f",
                paper_bgcolor="#1f1f1f",
                font=dict(color="white"),
            ),
        }

    filtered_data = import_data_long.copy()

    if selected_commodity and not selected_year:
        filtered_data = filtered_data[filtered_data["Commodity"] == selected_commodity]
        return {
            "data": [
                go.Scatter(
                    x=filtered_data["Year"],
                    y=filtered_data["Trade_Value"],
                    mode="lines+markers",
                    line=dict(color="yellow"),
                    marker=dict(size=8),
                )
            ],
            "layout": go.Layout(
                title=f"Import Trade Data for {selected_commodity}",
                xaxis={"title": "Year"},
                yaxis={"title": "Values in US$ Million"},
                yaxis_range=[0, filtered_data["Trade_Value"].max() * 1.1],
                plot_bgcolor="#1f1f1f",
                paper_bgcolor="#1f1f1f",
                font=dict(color="white"),
            ),
        }

    if selected_year and not selected_commodity:
        filtered_data = filtered_data[filtered_data["Year"] == selected_year]
        return {
            "data": [
                go.Bar(
                    x=filtered_data["Commodity"],
                    y=filtered_data["Trade_Value"],
                    marker=dict(color="yellow"),
                )
            ],
            "layout": go.Layout(
                title=f"Import Trade Data for {selected_year}",
                xaxis={"title": "Commodity"},
                yaxis={"title": "Values in US$ Million"},
                plot_bgcolor="#1f1f1f",
                paper_bgcolor="#1f1f1f",
                font=dict(color="white"),
            ),
        }

    return {
        "data": [],
        "layout": go.Layout(
            title="Select a Commodity or Year to Display Data",
            xaxis={"title": "Year or Commodity"},
            yaxis={"title": "Values in US$ Million"},
            plot_bgcolor="#1f1f1f",
            paper_bgcolor="#1f1f1f",
            font=dict(color="white"),
        ),
    }

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)

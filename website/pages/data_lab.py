import numpy as np
import pandas as pd
from io import StringIO
from pprint import pprint  # mostly for debugging
from datetime import date
import plotly.express as px
from base64 import b64decode
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, ALL, callback, callback_context as ctx, register_page


register_page(__name__, path="/data_lab", title="Data Laboratory", order=3)

MAIN_DATA: pd.DataFrame = pd.read_csv("data/total_data.csv", index_col="index")

MAIN_FILTERS = {"Date": "date-picker",
                "HomeTeam": "dropdown",
                "AwayTeam": "dropdown",
                "Pitcher": "dropdown",
                "Batter": "dropdown",
                "Inning": "range-slider"}

DATA_FILTERS = {"RelSpeed", "range-slider",
                "Outs", "dropdown"}

CHART_FILTERS = {"KorBB": "dropdown"}


def pre_process_data(df: pd.DataFrame) -> pd.DataFrame | None:
    if "Date" not in df.columns:
        return

    df = df.convert_dtypes()
    df["Date"] = pd.to_datetime(df["Date"]).dt.date

    df["TaggedPitchType"] = df["TaggedPitchType"].apply(lambda s: str(s).title())
    df["AutoPitchType"] = df["AutoPitchType"].apply(lambda s: str(s).title())

    return df


def str_to_date(s: str, sep: str = "-") -> date:
    if s is None:
        return date(2000, 1, 1)
    year, month, day = map(int, s.split(sep))
    return date(year, month, day)


@callback(
    Output("date-picker-range", "min_date_allowed"),
    Output("date-picker-range", "max_date_allowed"),
    Output("date-picker-range", "disabled_days"),
    Input("upload-data", "contents")
)
def add_data(*args):
    global MAIN_DATA

    files = args[0] or []
    total_data = MAIN_DATA.copy()

    for file in files:
        content_type, content_string = file.split(",")
        if "csv" not in content_type:
            continue
        decoded = b64decode(content_string)
        df = pd.read_csv(StringIO(decoded.decode('utf-8')))
        df = pre_process_data(df)
        if df is not None:
            total_data = pd.concat([df, total_data])

    total_data = total_data.drop_duplicates(ignore_index=True)
    total_data.to_csv("total_data.csv", index_label="index")
    MAIN_DATA = total_data

    start_date, end_date = MAIN_DATA["Date"].min(), MAIN_DATA["Date"].max()
    full_range = pd.date_range(start=start_date, end=end_date)
    missing_dates = full_range.difference(MAIN_DATA["Date"].unique()).tolist()

    return start_date, end_date, missing_dates


def dropdown(df: pd.DataFrame, col: str, _id: str | dict) -> tuple:
    options = sorted(df[col].unique())
    _id["widget"] = "Dropdown"
    label = html.Label(col)
    dd = dcc.Dropdown(options=options, value=False, multi=True, clearable=True, searchable=True,
                      placeholder=col + "(s)", id=_id, style={"width": "200px", "textAlign": "left"})
    return label, dd


def range_slider(df: pd.DataFrame, col: str, _id: str | dict, width: int = 200,
                 unit: str = "px") -> list[html.Label | dcc.Dropdown]:
    _id["widget"] = "RangeSlider"
    mn, mx = df[col].min(), df[col].max()
    step = 1 if "int" in str(df[col].dtype).lower() else 0.1
    marks = None
    if df[col].nunique() > 9:
        marks = np.linspace(mn, mx, 6)
        marks = {m: format(m, ".1f") for m in marks}
    label = html.Label(col)
    if marks:
        rs = dcc.RangeSlider(min=mn, max=mx, step=step, allowCross=False, tooltip={"placement": "bottom"},
                             marks=marks, id=_id)
    else:
        rs = dcc.RangeSlider(min=mn, max=mx, step=step, allowCross=False, tooltip={"placement": "bottom"},
                             id=_id)
    return [label, html.Div(rs, style={"width": f"{width}{unit}"})]


def date_picker(df: pd.DataFrame, col: str) -> tuple[dcc.DatePickerRange]:
    start_date = df[col].min()
    end_date = df[col].max()
    full_range = pd.date_range(start=start_date, end=end_date)
    missing_dates = full_range.difference(df[col].unique()).tolist()

    return (dcc.DatePickerRange(min_date_allowed=start_date, max_date_allowed=end_date, end_date=end_date,
                                start_date_placeholder_text="Start Date", end_date_placeholder_text="End Date",
                                display_format="MMM Do, YYYY", disabled_days=missing_dates, with_portal=True,
                                calendar_orientation="vertical", style={"margin": "10px"}, id="date-picker-range"),)


def column_filter(df: pd.DataFrame, col: str, component: str, width: int = 200, unit: str = "px"):
    if col not in df.columns:
        raise ValueError(f"Column {col} is not in the DataFrame, has \n{df.columns}")
    _id = {"type": "filter", "column": col, "widget": None}

    if component == "date-picker":
        col_filter = date_picker(df, col)
    elif component == "range-slider":
        col_filter = range_slider(df, col, _id, width, unit)
    elif component == "dropdown":
        col_filter = dropdown(df, col, _id)
    else:
        raise ValueError(f"component is not a valid option, got {component}")

    return col_filter


@callback(
    Output("filtered-graph", "figure"),
    Input({"type": "filter", "column": ALL, "widget": ALL}, "value"),
    Input("date-picker-range", "start_date"),
    Input("date-picker-range", "end_date"),
    Input("date-picker-range", "min_date_allowed"),
    Input("date-picker-range", "max_date_allowed")
)
def update_filters(*args):
    global MAIN_DATA

    # Retrieve input IDs and values
    triggered_inputs = {d["id"]["column"]: (d.get("value", None), d["id"]["widget"]) for d in ctx.inputs_list[0]}
    # pprint(triggered_inputs)
    start_date, end_date, min_date, max_date = args[-4:]
    start_date = start_date if start_date else min_date
    end_date = end_date if end_date else max_date

    # Start with the full DataFrame
    filtered_df = MAIN_DATA.copy()

    # Apply filtering based on each component's type (Dropdown or RangeSlider)
    for col_name, value_and_widget in triggered_inputs.items():
        value, widget = value_and_widget
        if widget == "RangeSlider" and value:  # RangeSlider values
            filtered_df = filtered_df[filtered_df[col_name].between(value[0], value[1])]
        elif widget == "Dropdown" and value:  # Dropdown values
            filtered_df = filtered_df[filtered_df[col_name].isin(value)]

    filtered_df = filtered_df[filtered_df["Date"].astype(str).between(start_date, end_date)]

    # Create and return the updated figure
    chart = px.scatter
    fig = chart(filtered_df, x='HorzBreak', y='InducedVertBreak', color="AutoPitchType", width=1000, height=700,
                hover_data=triggered_inputs.keys())
    return fig


layout = dbc.Container([
    # Header with Title, Subtitle, and Upload box
    dbc.Row([
        dbc.Col([
            html.H1("Trackman Visualizer", className="text-center"),
            dcc.Upload(
                id='upload-data',
                children=html.Div([html.Center([
                    'Drag and Drop or ',
                    html.A('Select Files', style={"text-decoration": "underline"})
                ])]),
                style={
                    'width': '100%',
                    'height': '50px',
                    'lineHeight': '50px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'margin': '10px'
                },
                multiple=True,
                accept=".csv"
            )
        ])
    ]),

    # Row of Dropdowns, RangeSliders, and DatePickerRange
    dbc.Row([
        dbc.Col(column_filter(MAIN_DATA, col, component), width=12 // len(MAIN_FILTERS))
        for col, component in MAIN_FILTERS.items()
    ], style={"padding": "10px", "alignItems": "left"}),

    # Main content with 3 columns
    dbc.Row([
        # Left-most column
        dbc.Col([
            html.H4("Chart Properties"),
            # *[column_filter(MAIN_DATA, col, component)[-1] for col, component in CHART_FILTERS.items()]
        ], width=2),

        # Center column
        dbc.Col([
            dbc.Row([
                dbc.Col(html.Label("Charts"), width=3),
                dbc.Col(html.Label("Presets"), width=3)
            ], align="left"),
            dbc.Row([
                dbc.Col(dcc.Dropdown(id='plotly-chart-dropdown',
                                     options=[{'label': f'Option {i}', 'value': i} for i in range(5)],
                                     placeholder="Plotly Charts",
                                     style={"width": "200px"})),
                dbc.Col(dcc.Dropdown(id='preset-chart-dropdown',
                                     options=[{'label': f'Option {i}', 'value': i} for i in range(5)],
                                     placeholder="Preset Charts",
                                     style={"width": "200px"}))
            ], align="left"),
            dcc.Graph(id="filtered-graph")
        ], width=8),

        # Right-most column
        dbc.Col([
            html.H4("Data Filters"),
            *column_filter(MAIN_DATA, "AutoPitchType", "dropdown"),
            *column_filter(MAIN_DATA, "RelSpeed", "range-slider", 100, "%"),
            *column_filter(MAIN_DATA, "Outs", "dropdown"),
            dcc.Checklist(
                id='checkbox-dropdown',
                options=[
                    {'label': 'Option 1', 'value': 'option1'},
                    {'label': 'Option 2', 'value': 'option2'},
                    {'label': 'Option 3', 'value': 'option3'}
                ],
                value=[],  # Default selected values
                labelStyle={'display': 'block'}  # Display each item on a new line
            )
            # Additional dropdowns and sliders can be added here
        ], width=2)
    ], style={'padding': '20px'})
], fluid=True)

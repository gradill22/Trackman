from dash import Dash, page_registry, html, dcc, page_container

# Initialize the Dash app
app = Dash(__name__, use_pages=True, pages_folder="pages")  # Enable multi-page support

# Default layout includes navigation
app.layout = html.Div([
    html.H1("Trackman Visualizer", style={"textAlign": "center"}),
    html.Nav([
        dcc.Link(page["title"], href=page["path"])
        for _, page in page_registry.items()
    ]),
    page_container
])


if __name__ == "__main__":
    for k, v in page_registry.items():
        print(f"{k} => {v}")
    print("Page container:", page_container, sep="\n")
    app.run_server(debug=True)

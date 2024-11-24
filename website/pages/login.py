from dash import html, register_page, dcc

register_page(__name__, path="/login", title="Login", order=2)

layout = html.Div([
    html.H2("Login Page"),
    html.Form([
        html.Label("Username"),
        dcc.Input(type="text", id="username"),
        html.Label("Password"),
        dcc.Input(type="password", id="password"),
        html.Button("Login", id="login-button"),
    ])
])

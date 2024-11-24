from dash import html, register_page

register_page(__name__, path="/account", title="Account", order=4)

layout = html.Div([
    html.H2("Account Page"),
    html.P("Manage your account settings here.")
])

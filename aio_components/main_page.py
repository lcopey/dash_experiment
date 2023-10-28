import dash_bootstrap_components as dbc
from aio.pagewithsidebar import PageWithSideBar
from dash import Dash

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = PageWithSideBar("Test", "Sidebar Test", "page", side_bar_width="20%")

if __name__ == "__main__":
    app.run(debug=True)

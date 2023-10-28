import dash_bootstrap_components as dbc
from aio.page_with_section import PageWithSection, Section
from aio.page_with_sidebar import PageWithSideBar
from dash import Dash, html

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# app.layout = PageWithSideBar("Test", "Sidebar Test", "page", side_bar_width="20%")
sections = [Section("Section 1", ["Section 1"]), Section("Section 2", ["Section 2"])]
app.layout = PageWithSection("page", sections)

if __name__ == "__main__":
    app.run(debug=True)

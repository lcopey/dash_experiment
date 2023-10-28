from dataclasses import dataclass

import dash_bootstrap_components as dbc
from dash import html

from .page_with_sidebar import PageWithSideBar, PageWithSideBarIds


class PageWithSectionIds(PageWithSideBarIds):
    pass


@dataclass
class Section:
    title: str
    children: list


def get_summary_div(section: Section):
    return html.Details([html.Summary(section.title), *section.children])


class PageWithSection(PageWithSideBar):
    def __init__(
        self, aio_id: str, sections: list[Section], side_bar_width: str = "20%"
    ):
        side_bar_child = dbc.Nav(
            [
                dbc.NavLink(section.title, href="/", active="exact")
                for section in sections
            ],
            vertical=True,
            pills=True,
        )
        main_page_child = [get_summary_div(section) for section in sections]
        super().__init__(
            aio_id=aio_id,
            side_bar_width=side_bar_width,
            side_bar_children=[html.Hr(), side_bar_child, html.Hr()],
            main_page_children=main_page_child,
        )

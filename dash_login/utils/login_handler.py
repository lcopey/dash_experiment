from dash import page_registry

RESTRICTED_PAGES = {}


def require_login(page):
    for pg in page_registry:
        if page == pg:
            RESTRICTED_PAGES[page_registry[pg]["path"]] = True

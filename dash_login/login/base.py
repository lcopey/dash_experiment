import os

from dash import ALL, Dash, Input, Output, dcc, html, no_update, page_container
from dotenv import load_dotenv
from flask import Flask, redirect, request, session
from utils import RESTRICTED_PAGES

from aio_components.aio.ids import BaseId, auto


class FlaskSession:
    @staticmethod
    def is_logged():
        return "logged" in session and session["logged"]

    @staticmethod
    def current_user():
        return "user" in session and session["user"]

    @staticmethod
    def set_user(username: str):
        session["logged"] = True
        session["user"] = username

    @staticmethod
    def logout():
        session["logged"] = False
        session["user"] = None


class AppId(BaseId):
    user_status_header = auto()
    url = auto()
    redirect = auto()


class ProtectedDash(Dash):
    def __init__(self):
        load_dotenv()

        server = Flask(__name__)
        server.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

        super().__init__(
            __name__, server=server, use_pages=True, pages_folder="../pages"
        )

        self.ids = AppId("app")
        self.layout = html.Div(
            [
                dcc.Location(id=self.ids.url),
                html.Div(id=self.ids.user_status_header),
                html.Hr(),
                page_container,
            ]
        )

        @self.server.route("/login", methods=["POST"])
        def login():
            if request.form:
                username = request.form["username"]
                password = request.form["password"]
                if username == "laurent":
                    if "url" in session:
                        url = session["url"]
                        session["url"] = None
                        FlaskSession.set_user(username)
                        return redirect(url)
                    else:
                        return redirect("/")

            return redirect("login")

        # @self.server.route('/logout', methods=['GET'])
        # def on_logout():
        #     logout()
        #     return redirect('login')

        @self.callback(
            Output(self.ids.user_status_header, "children"),
            Output(self.ids.url, "pathname"),
            Input(self.ids.url, "pathname"),
            # Input({'index': ALL, 'type': ids.redirect}, 'n_intervals')
        )
        # def update_authentication_status(path, n):
        def update_authentication(path):
            ### logout redirect
            # if n:
            #     if not n[0]:
            #         return '', no_update
            #     else:
            #         return '', '/login'

            # test if user is logged in
            if FlaskSession.is_logged():
                if path == "/login":
                    return dcc.Link("logout", href="/logout"), "/"
                return dcc.Link("logout", href="/logout"), no_update
            else:
                # if page is restricted, redirect to login and save path
                if path in RESTRICTED_PAGES:
                    session["url"] = path
                    return dcc.Link("login", href="/login"), "/login"

            # if path not login and logout display login link
            if FlaskSession.current_user() and path not in ["/login", "/logout"]:
                return dcc.Link("login", href="/login"), no_update

            # if path login and logout hide links
            if path in ["/login", "/logout"]:
                return "", no_update

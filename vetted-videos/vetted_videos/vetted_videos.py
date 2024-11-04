import functools
import json
import os
import time
from .backend.backend import State
from google.auth.transport import requests
from google.oauth2.id_token import verify_oauth2_token
import os.path
import reflex as rx
from .pages.home import home

from .react_oauth_google import (
    GoogleOAuthProvider,
    GoogleLogin,
)

def user_info(tokeninfo: dict) -> rx.Component:
    return rx.hstack(
        rx.avatar(
            name=tokeninfo["name"],
            src=tokeninfo["picture"],
            size="lg",
        ),
        rx.vstack(
            rx.heading(tokeninfo["name"], size="md"),
            rx.text(tokeninfo["email"]),
            align_items="flex-start",
        ),
        rx.button("Logout", on_click=State.logout),
        padding="10px",
    )


def login() -> rx.Component:
    return rx.vstack(
        GoogleLogin.create(on_success=State.on_success),
    )


def require_google_login(page) -> rx.Component:
    @functools.wraps(page)
    def _auth_wrapper() -> rx.Component:
        return GoogleOAuthProvider.create(
            rx.cond(
                State.is_hydrated,
                rx.cond(
                    State.token_is_valid, page(), login()
                ),
                rx.spinner(),
            ),
            client_id=State.CLIENT_ID,
        )

    return _auth_wrapper


def index():
    return rx.center(
        rx.vstack(
        rx.heading("Vetted Videos", size="lg"),
        rx.link("Go To Login", href="/protected"),
    )
    )


@rx.page(route="/protected")
@require_google_login
def protected() -> rx.Component:
    return rx.center(rx.vstack(
        user_info(State.tokeninfo),
        rx.center(rx.vstack(
        rx.vstack(State.protected_content),
        rx.link("Back", href="/"),))
    ))


app = rx.App()
app.add_page(index)
app.add_page(home, route="/home")


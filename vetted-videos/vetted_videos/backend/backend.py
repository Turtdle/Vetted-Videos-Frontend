import functools
import json
import os
import time

from google.auth.transport import requests
from google.oauth2.id_token import verify_oauth2_token
import os.path
import reflex as rx

from ..react_oauth_google import (
    GoogleOAuthProvider,
    GoogleLogin,
)


class State(rx.State):
    CLIENT_ID = ""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.CLIENT_ID = ""
        client_id_path = os.path.join(os.path.dirname(__file__), "..", "..", "client_id")
        if os.path.exists(client_id_path):
            with open(client_id_path) as f:
                self.CLIENT_ID = f.read().strip()
        
    id_token_json: str = rx.LocalStorage()

    def on_success(self, id_token: dict):
        self.id_token_json = json.dumps(id_token)

    @rx.var(cache=True)
    def tokeninfo(self) -> dict[str, str]:
        try:
            return verify_oauth2_token(
                json.loads(self.id_token_json)[
                    "credential"
                ],
                requests.Request(),
                self.CLIENT_ID,
            )
        except Exception as exc:
            if self.id_token_json:
                print(f"Error verifying token: {exc}")
        return {}

    def logout(self):
        self.id_token_json = ""

    @rx.var
    def token_is_valid(self) -> bool:
        try:
            return bool(
                self.tokeninfo
                and int(self.tokeninfo.get("exp", 0))
                > time.time()
            )
        except Exception:
            return False

    @rx.var(cache=True)
    def protected_content(self) -> rx.Component:
        if self.token_is_valid:
            return rx.link(
                "Example",
                href="home",
            )
        return rx.button(
        "open in tab",
        on_click=rx.redirect(
            "/docs/api-reference/special_events"
        ),
    )
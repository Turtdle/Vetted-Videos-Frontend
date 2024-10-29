from ..backend.backend import State
import reflex as rx
def home() -> rx.Component:
    return rx.text(f"This content can only be viewed by a logged in User. Nice to see you {State.tokeninfo['name']}")
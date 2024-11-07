from ..backend.backend import State
import reflex as rx
from ..components.form_field import form_field
from ..views.table import main_table, _add_item_button
def home() -> rx.Component:
    return rx.cond(
    State.token_is_valid,
        rx.vstack(
            _add_item_button(),
            main_table()
        ),
        rx.center(
            rx.text("Please Login at main page"),
        )
    )
    
    
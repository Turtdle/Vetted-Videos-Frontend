from ..backend.backend import State
import reflex as rx
from ..components.form_field import form_field
def home() -> rx.Component:
    return rx.cond(
        State.token_is_valid,
        rx.dialog.root(
        rx.dialog.trigger(
            rx.center(
            rx.button(
                rx.icon("plus", size=26),
                rx.text("Add Video", size="4", display=["none", "none", "block"]),
                size="3",
            )),
        ),
        rx.dialog.content(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="box", size=34),
                    color_scheme="blue",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.dialog.title(
                        "Add Video",
                        weight="bold",
                        margin="0",
                    ),
                    rx.dialog.description(
                        "Fill the form with the video's info",
                    ),
                    spacing="1",
                    height="100%",
                    align_items="start",
                ),
                height="100%",
                spacing="4",
                margin_bottom="1.5em",
                align_items="center",
                width="100%",
            ),
            rx.form.root(
                rx.flex(
                    rx.vstack(
                        form_field(
                            "Username",
                            "Username",
                            "text",
                            "username",
                            "box",
                        ),
                        form_field(
                            "Video Name",
                            "Video Name",
                            "text",
                            "videoname",
                            "box",
                        ),
                        form_field(
                            "Length",
                            "Length",
                            "text",
                            "length",
                            "box",
                        ),form_field(
                            "Thumbnail",
                            "URL",
                            "text",
                            "thumbnail",
                            "box",
                        ),
                        form_field(
                            "Product Name",
                            "Product Name",
                            "text",
                            "product",
                            "box",
                        ),form_field(
                            "Video",
                            "Link",
                            "text",
                            "link",
                            "box",
                        ),form_field(
                            "Tags",
                            "Seperate tags by commas",
                            "text",
                            "tags",
                            "box",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                variant="soft",
                                color_scheme="gray",
                            ),
                        ),
                        rx.form.submit(
                            rx.dialog.close(
                                rx.button("Submit Item"),
                            ),
                            as_child=True,
                        ),
                        padding_top="2em",
                        spacing="3",
                        mt="4",
                        justify="end",
                    ),
                    width="100%",
                    direction="column",
                    spacing="4",
                ),
                on_submit=State.add_item,
                reset_on_submit=True,
            ),
            width="100%",
            max_width="450px",
            justify=["end", "end", "start"],
            padding="1.5em",
            border=f"2.5px solid {rx.color('accent', 7)}",
            border_radius="25px",
        ),
    ),
        rx.text(f"Please Login")
    )
    
    
    
import reflex as rx
from ..backend.backend import State, VideoData
from typing import TypedDict
from ..components.form_field import form_field
def _header_cell(text: str, icon: str):
    return rx.table.column_header_cell(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text),
            align="center",
            spacing="2",
        ),
    )

def _add_item_button() -> rx.Component:
    return rx.box(
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
        )

def _update_video_dialog(video: VideoData):
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.icon_button(
                rx.icon("square-pen", size=22),
                color_scheme="green",
                size="2",
                variant="solid",
                on_click=lambda: State.set_video_to_update(video),
            ),
        ),
        rx.dialog.content(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="square-pen", size=34),
                    color_scheme="blue",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.dialog.title(
                        "Edit Item",
                        weight="bold",
                        margin="0",
                    ),
                    rx.dialog.description(
                        "Edit the videos's info",
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
                    rx.hstack(
                        form_field(
                            "Name",
                            "Item Name",
                            "text",
                            "item_name",
                            "box",
                            str(video["videname"]),  # fuck
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
                                rx.button("Update Item"),
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
                on_submit=State.update_item,
                reset_on_submit=False,
            ),
            max_width="450px",
            padding="1.5em",
            border=f"2px solid {rx.color('accent', 7)}",
            border_radius="25px",
        ),
    )

def _show_item(item: VideoData):
    return rx.table.row(
        rx.table.cell(item["videoname"]),
        rx.table.cell(item["username"]),
        rx.table.cell(item["product"]),
        rx.table.cell(item["docid"]),
        rx.table.cell(
            rx.hstack(
                _update_video_dialog(item),
                rx.icon_button(
                    rx.icon("trash-2", size=22),
                    color_scheme="red",
                    size="2",
                    variant="solid",
                    on_click=lambda: State.delete_item(item),
                ),
                spacing="2",
            )
        ),
    )

def main_table():
    return rx.fragment(
        rx.flex(
            #_add_item_button(),
            rx.spacer(),
            rx.cond(
                #State.sort_reverse,
                rx.icon(
                    "arrow-down-z-a",
                    size=28,
                    stroke_width=1.5,
                    cursor="pointer",
                    #on_click=State.toggle_sort,
                ),
                rx.icon(
                    "arrow-down-a-z",
                    size=28,
                    stroke_width=1.5,
                    cursor="pointer",
                    #on_click=State.toggle_sort,
                ),
            ),
            rx.select(
                ["item_name"],
                placeholder="Sort By: Name",
                size="3",
                #on_change=lambda sort_value: State.sort_values(sort_value),
            ),
            rx.input(
                rx.input.slot(rx.icon("search")),
                placeholder="Search here...",
                size="3",
                max_width="225px",
                width="100%",
                variant="surface",
                #on_change=lambda value: State.filter_values(value),
            ),
            justify="end",
            align="center",
            spacing="3",
            wrap="wrap",
            width="100%",
            padding_bottom="1em",
        ),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    _header_cell("Video Name", "box"),
                    _header_cell("Username", "box"),
                    _header_cell("Product Name", "box"),
                    #_header_cell("Doc ID", "box"),
                    _header_cell("Actions", "cog"),
                    
                ),
            ),
            rx.table.body(rx.foreach(State.videos, _show_item)),
            variant="surface",
            size="3",
            width="100%",
        ),
    )
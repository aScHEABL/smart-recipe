import reflex as rx

from rxconfig import config


class State(rx.State):
    ...


def index() -> rx.Component:
    # 首頁 (Index)
    return rx.container(
            rx.center(
                rx.input(rx.input.slot(rx.icon("search")),
                            placeholder="搜尋食譜",
                            type="search",
                            size="3",
                            width="400px",
                        ),
            )
    )


app = rx.App()
app.add_page(index)

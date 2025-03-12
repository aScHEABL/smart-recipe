import reflex as rx
import httpx

from rxconfig import config


class State(rx.State):
    query: str = ""
    meals: list = []

    async def search(self, query: str):
        self.query = query
        if not query:
            self.meals = []
            print("User clears query")
            return

        async with httpx.AsyncClient() as client:
            response = await client.get(f'https://www.themealdb.com/api/json/v1/1/search.php?s={self.query}')
            if response.status_code == 200:
                data = response.json()
                self.meals = data.get("meals", [])
                print(self.meals)
            else:
                self.meals = []

def index() -> rx.Component:
    # 首頁 (Index)
    return rx.container(
            rx.center(
                rx.input(rx.input.slot(rx.icon("search")),
                            placeholder="搜尋食譜",
                            type="search",
                            size="3",
                            width="400px",
                            on_change=State.search
                        ),
            )
    )


app = rx.App()
app.add_page(index)

import reflex as rx
import httpx

from rxconfig import config


class State(rx.State):
    # 儲存這些變數在Component state裡面
    query: str = ""
    meals: list[dict] = []
    render_menu: bool = False

    async def search(self, query: str):
        self.query = query

        # 如果欄位為空，停止渲染搜尋結果
        if not query:
            self.meals = []
            self.render_menu = False
            print("User clears query")
            return

        async with httpx.AsyncClient() as client:
            response = await client.get(f'https://www.themealdb.com/api/json/v1/1/search.php?s={self.query}')
            if response.status_code == 200:
                data = response.json()
                self.meals = data.get("meals", [])
                self.render_menu = True
            else:
                # 如果搜尋不到，停止宣染搜尋結果
                self.meals = []
                self.render_menu = False

def ReusableCard(item: rx.Var):
    return rx.cond(
                State.render_menu,
                    rx.card(
                        rx.link(
                            rx.image(src=item.strMealThumb),
                            href=item.strYoutube.to(str),
                            is_external=True,
                        ),
                        rx.heading(
                            item.strMeal, 
                            size="4", 
                            align="center",
                            padding_top="1em",
                        ),
                    ),
            )

                

def index() -> rx.Component:
    # 首頁 (Index)
    return rx.container(
            rx.center(
                rx.input(rx.input.slot(rx.icon("search")),
                            placeholder="輸入英文食譜名子",
                            type="search",
                            size="3",
                            width="400px",
                            on_change=State.search,
                        ),
                rx.grid(
                        rx.foreach(State.meals, ReusableCard),
                        columns="2",
                        spacing="4",
                        width="80%",
                    ),
                wrap="wrap",
                spacing="4",
            )
    )


app = rx.App()
app.add_page(index)

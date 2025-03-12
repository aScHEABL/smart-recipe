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
                rx.fragment(
                    rx.flex(
                        rx.card(
                            rx.link(
                                rx.image(src=item.strMealThumb, width="200px"),
                                href=item.strYoutube.to(str),
                                is_external=True,
                            ),
                        ),
                        rx.heading(item.strMeal),
                        wrap="wrap",
                    )
                ), # 條件式宣染，故意留白
            )

                

def index() -> rx.Component:
    # 首頁 (Index)
    return rx.container(
            rx.center(
                rx.input(rx.input.slot(rx.icon("search")),
                            placeholder="搜尋食譜",
                            type="search",
                            size="3",
                            width="400px",
                            on_change=State.search,
                        ),
                rx.flex(rx.foreach(State.meals, ReusableCard),
                            wrap="wrap",
                            justify="center",
                        ),
                wrap="wrap",
            )
    )


app = rx.App()
app.add_page(index)

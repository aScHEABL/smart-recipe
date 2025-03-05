#!/usr/bin/env python3
import asyncio
from typing import Optional

import httpx

from nicegui import events, ui

api = httpx.AsyncClient()
running_query: Optional[asyncio.Task] = None


async def search(e: events.ValueChangeEventArguments) -> None:
    """輸入就執行搜尋"""
    global running_query  # pylint: disable=global-statement # noqa: PLW0603
    if running_query:
        running_query.cancel()  # 當使用者輸入很快的時候取消掉之前的搜尋
    results.clear()

    running_query = asyncio.create_task(api.get(f'https://www.themealdb.com/api/json/v1/1/search.php?s={e.value}'))
    response = await running_query
    if response.text == '':
        return
    with results:
        for meal in response.json()['meals'] or []:
            with ui.image(meal['strMealThumb']).classes('w-64'):
                ui.label(meal['strMeal']).classes('absolute-bottom text-subtitle2 text-center')
    running_query = None

# 創見一個上方有空位的搜尋欄
search_field = ui.input(on_change=search) \
    .props('autofocus outlined rounded item-aligned input-class="ml-3"') \
    .classes('w-96 self-center mt-2 transition-all')
results = ui.row()

ui.run()
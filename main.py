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
            with ui.image(meal['strMealThumb']).classes('w-48'):
                ui.label(meal['strMeal']).classes('absolute-bottom text-subtitle2 text-center')
    running_query = None

ui.query('body').classes('flex justify-center bg-zinc-800')
ui.query('.nicegui-content').classes('p-0 gap-0')

# 創建一個上方有空位的搜尋欄
with ui.element('header').classes('flex justify-center bg-white rounded-t'):
    search_field = ui.input(on_change=search) \
        .props('autofocus outlined rounded item-aligned input-class="ml-3"') \
        .classes('w-[28rem]')

with ui.element('div').classes('w-96 w-[28rem] bg-white h-[100vh] rounded-b'):
    results = ui.element('div').classes('flex justify-center gap-4')

ui.run()
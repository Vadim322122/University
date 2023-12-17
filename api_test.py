import aiohttp
from utils.api import AsyncExpenseClient
from datetime import datetime
import asyncio

async def main():
    client = AsyncExpenseClient('http://localhost:8000/api')

    # Создание расхода
    new_expense = await client.create_expense('Обед', 'Поход в кафе', 15.00, datetime.now(), 'Еда')
    print(new_expense)

    # Получение всех расходов
    all_expenses = await client.get_expenses()
    print(all_expenses)

    # Получение расхода по ID
    expense_detail = await client.get_expense(new_expense['id'])
    print(expense_detail)

    # Обновление расхода
    updated_expense = await client.update_expense(new_expense['id'], title='Обед')
    print(updated_expense)

    # Удаление расхода
    deleted_response = await client.delete_expense(new_expense['id'])
    print(deleted_response)

    # Получение расходов по категории
    food_expenses = await client.get_expenses_by_category('Еда')
    print(food_expenses)

    # Получение расходов за определенный период
    expenses_date_range = await client.get_expenses_in_date_range(datetime(2023, 1, 1), datetime(2023, 12, 31))
    print(expenses_date_range)

asyncio.run(main())
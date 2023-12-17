import aiohttp
from datetime import datetime, timedelta
from collections import Counter

class AsyncExpenseClient:
    def __init__(self, base_url):
        self.base_url = base_url

    async def create_expense(self, title, description, amount, date, category):
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/expenses/"
            data = {
                "title": title,
                "description": description,
                "amount": amount,
                "date": date.strftime('%Y-%m-%d'),
                "category": category
            }
            async with session.post(url, json=data) as response:
                return await response.json()

    async def get_expenses(self, start_date=None, end_date=None, category=None):
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/expenses/"
            params = {}
            if start_date:
                params['start_date'] = start_date.strftime('%Y-%m-%d')
            if end_date:
                params['end_date'] = end_date.strftime('%Y-%m-%d')
            if category:
                params['category'] = category

            async with session.get(url, params=params) as response:
                return await response.json()

    async def get_expense(self, expense_id):
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/expenses/{expense_id}/"
            async with session.get(url) as response:
                return await response.json()

    async def update_expense(self, expense_id, title=None, description=None, amount=None, date=None, category=None):
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/expenses/{expense_id}/"
            data = {}
            if title is not None:
                data['title'] = title
            if description is not None:
                data['description'] = description
            if amount is not None:
                data['amount'] = amount
            if date is not None:
                data['date'] = date.strftime('%Y-%m-%d')
            if category is not None:
                data['category'] = category

            async with session.patch(url, json=data) as response:
                return await response.json()

    async def delete_expense(self, expense_id):
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/expenses/{expense_id}/"
            async with session.delete(url) as response:
                if response.status == 204:
                    return {"message": "Expense deleted successfully"}
                else:
                    return await response.json()

    async def get_expenses_by_category(self, category):
        return await self.get_expenses(category=category)

    async def get_expenses_in_date_range(self, start_date, end_date):
        return await self.get_expenses(start_date=start_date, end_date=end_date)

    async def get_expenses_last_30_days(self):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        return await self.get_expenses(start_date=start_date, end_date=end_date)

    async def count_expenses_last_30_days(self):
        expenses = await self.get_expenses_last_30_days()
        return len(expenses)

    async def sum_expenses_last_30_days(self):
        expenses = await self.get_expenses_last_30_days()
        return sum(expense['amount'] for expense in expenses)

    async def most_common_category_last_30_days(self):
        expenses = await self.get_expenses_last_30_days()
        categories = [expense['category'] for expense in expenses]
        most_common = Counter(categories).most_common(1)
        return most_common[0][0] if most_common else None
import logging
from handlers.admin import admin
from database import db
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config.config import Config
import asyncio

logging.basicConfig(level=logging.INFO)

class AiogramInstance:
    dispatcher_instance = None
    bot_instance = None

    @staticmethod
    async def get_instance():
        config = Config(1, "config.ini")
        if AiogramInstance.dispatcher_instance is None:
            token = await config.get('BOT_TOKEN', 'token')
            bot = Bot(token=token)
            AiogramInstance.dispatcher_instance = Dispatcher(bot, storage=MemoryStorage())
            AiogramInstance.bot_instance = bot
        return [AiogramInstance.dispatcher_instance, AiogramInstance.bot_instance]

async def startup():
    await db.start_db()

    list = await AiogramInstance.get_instance()
    dp, bot = list
    print('Aiogram started')

    await asyncio.gather(dp.start_polling(), admin.setup_handlers(dp, bot))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(startup())
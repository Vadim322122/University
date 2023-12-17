from filters.admin_filter import IsAdmin
from config.config import Config
from database import db
from utils.api import AsyncExpenseClient
from states.bot_states import Creation

from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.storage import FSMContext
from aiogram import Bot, Dispatcher
from aiogram import types
import aiogram

async def setup_handlers(dp: Dispatcher, bot: Bot):
    @dp.message_handler(commands=["start"])
    async def start(message: types.Message):
        language_code = await db.get_language(message.from_user.id)
        if language_code is None:
            language_code = 'ua'
        config = Config(message.from_user.id, f"languages/{language_code}.ini")
        
        text = await config.get('MAIN_MENU', 'text')
        
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text=await config.get('MAIN_MENU', 'button_spend_list'), callback_data='button_spend_list'))
        keyboard.add(InlineKeyboardButton(text=await config.get('MAIN_MENU', 'button_create_spend'), callback_data='button_create_spend'))
        keyboard.add(InlineKeyboardButton(text=await config.get('MAIN_MENU', 'button_del_spend'), callback_data='button_del_spend'))
        keyboard.add(InlineKeyboardButton(text=await config.get('MAIN_MENU', 'button_stats'), callback_data='button_stats'))
        keyboard.add(InlineKeyboardButton(text=await config.get('MAIN_MENU', 'button_faq'), callback_data='faq'))

        await message.answer(text, reply_markup=keyboard)

    @dp.message_handler(state='*', content_types=types.ContentType.ANY)
    async def procces_message(message: types.Message, state: FSMContext):
        language_code = await db.get_language(message.from_user.id)
        if language_code is None:
            language_code = 'ua'
        config = Config(message.from_user.id, f"languages/{language_code}.ini")
        client = AsyncExpenseClient("http://localhost:8000")
        state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
        current_state = await state.get_state()

    @dp.callback_query_handler(state='*')
    async def procces_callback(callback: types.CallbackQuery, state: FSMContext):
        language_code = await db.get_language(callback.from_user.id)
        if language_code is None:
            language_code = 'ua'
        config = Config(callback.from_user.id, f"languages/{language_code}.ini")
        
        client = AsyncExpenseClient("http://localhost:8000")
        if callback.data == 'button_spend_list':
            get_expenses = await client.get_expenses()
            
            text = await config.get('SPEND_LIST', 'text')
            go_main_menu = await config.get('GO_BACK', 'go_main_menu')
            
            keyboard = InlineKeyboardMarkup()
            for expense in get_expenses:
                keyboard.add(InlineKeyboardButton(text=expense['title'], callback_data=f"expense_{expense['id']}"))
            keyboard.add(InlineKeyboardButton(text=go_main_menu, callback_data=f'go_main_menu'))
            
            await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text=text, reply_markup=keyboard)
        
        elif callback.data.startswith('expense_'):
            id = callback.data.split('_')[1]
            info = await client.get_expense(id)
            text_id = await config.get('SPEND_LIST', 'text_id') + str(info['id'])
            text_title = await config.get('SPEND_LIST', 'text_title') + str(info['title'])
            text_desc = await config.get('SPEND_LIST', 'text_desc') + str(info['description'])
            text_sum = await config.get('SPEND_LIST', 'text_sum') + str(info['amount'])
            text_date = await config.get('SPEND_LIST', 'text_date') + str(info['date'])
            
            result = f"{text_id}\n{text_title}\n{text_desc}\n{text_sum}\n{text_date}"
            
            go_main_menu = await config.get('GO_BACK', 'go_main_menu')
            
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text=go_main_menu, callback_data=f'go_main_menu'))
            
            await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text=result, reply_markup=keyboard)
        
        elif callback.data == 'button_create_spend':
            text = await config.get('CREATE_SPEND', 'text')
            
            go_main_menu = await config.get('GO_BACK', 'go_main_menu')
            
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text=go_main_menu, callback_data=f'go_main_menu'))
            
            await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text=text, reply_markup=keyboard)
        
        elif callback.data == 'button_del_spend':
            text = await config.get('DELETE_SPEND', 'text')
            
            go_main_menu = await config.get('GO_BACK', 'go_main_menu')
            
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text=go_main_menu, callback_data=f'go_main_menu'))
            
            await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text=text, reply_markup=keyboard)
        
        elif callback.data == 'button_stats':
            text_count = await config.get('STATS', 'text_count') + str(await client.count_expenses_last_30_days())
            text_sum = await config.get('STATS', 'text_sum') + str(await client.sum_expenses_last_30_days())
            text_cat = await config.get('STATS', 'text_cat') + str(await client.most_common_category_last_30_days())
            
            result = f"{text_count}\n{text_sum}\ntext_cat"
            
            go_main_menu = await config.get('GO_BACK', 'go_main_menu')
            
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text=go_main_menu, callback_data=f'go_main_menu'))
            
            await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text=result, reply_markup=keyboard)
            
        elif callback.data == 'faq':
            text = await config.get('FAQ', 'text')
            go_main_menu = await config.get('GO_BACK', 'go_main_menu')
            
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text=go_main_menu, callback_data=f'go_main_menu'))
            
            await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text=text, reply_markup=keyboard)
        
        elif callback.data == 'go_main_menu':
            text = await config.get('MAIN_MENU', 'text')
            
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text=await config.get('MAIN_MENU', 'button_spend_list'), callback_data='button_spend_list'))
            keyboard.add(InlineKeyboardButton(text=await config.get('MAIN_MENU', 'button_create_spend'), callback_data='button_create_spend'))
            keyboard.add(InlineKeyboardButton(text=await config.get('MAIN_MENU', 'button_del_spend'), callback_data='button_del_spend'))
            keyboard.add(InlineKeyboardButton(text=await config.get('MAIN_MENU', 'button_stats'), callback_data='button_stats'))
            keyboard.add(InlineKeyboardButton(text=await config.get('MAIN_MENU', 'button_faq'), callback_data='faq'))
            
            await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text=text, reply_markup=keyboard)
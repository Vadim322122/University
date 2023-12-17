from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def create_inline_keyboard(items: list, start_callback: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for item in items:
        callback_data = f"{start_callback}{item[0]}"
        buttons.append(InlineKeyboardButton(text=item[1], callback_data=callback_data))

    for i in range(0, len(buttons), 2):
        row = buttons[i:i+2]
        keyboard.add(*row)

    return keyboard
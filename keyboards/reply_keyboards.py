from aiogram import types

async def sep_by_2(button_texts):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if len(button_texts) % 2 == 0:
        for i in range(0, len(button_texts), 2):
            kb.add(types.KeyboardButton(button_texts[i]), types.KeyboardButton(button_texts[i+1]))
    else:
        for i in range(0, len(button_texts)-1, 2):
            kb.add(types.KeyboardButton(button_texts[i]), types.KeyboardButton(button_texts[i+1]))
        kb.add(types.KeyboardButton(button_texts[-1]))
    return kb

async def sep_by_1(button_texts):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton(button_texts))
    return kb
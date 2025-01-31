from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from core.config import ADMIN_ID


def opportunity_cancel_nick():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text='Продолжить без псевдонима😶‍🌫️')]
    ])
    return markup

def keyboard_get_confirm():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text='Подтвердить✅'), KeyboardButton(text='Изменить✏️')],
        [KeyboardButton(text='Отмена❌')]
    ])
    return markup

def cancel_kb_txt():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text='Без текста✏️')],
        [KeyboardButton(text='Отмена❌')]
    ])
    return markup

def cancel_kb_media():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text='Без фото📷')],
        [KeyboardButton(text='Отмена❌')]
    ])
    return markup

def keyboard_de_unknown_sender(refer):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Узнать отправителя🔍', callback_data=f'&_{refer}')]
    ])
    return markup

def keyboard_pay(tg_id):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Оплатить💰', pay=True)],
        [
            InlineKeyboardButton(text='Отменить оплату❌', callback_data='cancel'),
            InlineKeyboardButton(text='Оплатить Деанонами🫣', callback_data=tg_id)]
    ])
    return markup

def anonimshik():
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='По другим вопросам или Предложениям обращайтесь сюда', url=f'tg://user?id={ADMIN_ID}')]
    ])
    return markup

def hyper_link_profile(tg_id, text='По другим вопросом обращайтесь сюда'):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text, url=f'tg://user?id={tg_id}')]
    ])
    return markup

def kb_de_unknowns(unused_refs, de_unknowns):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f'{unused_refs}  👤', callback_data=' '),
            InlineKeyboardButton(text=f'{de_unknowns}  🫣', callback_data=' ')
        ],
        [InlineKeyboardButton(text='✨Обменять награды✨', callback_data=f'exchange_{unused_refs}')]
    ])
    return markup
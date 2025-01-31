from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, InputMediaPhoto, InputMediaVideo

from core.data.postgres import PgSql
from core.utils.media_builder import media_assembler
from core.utils.state_machine import SaveSteps
from core.utils.keyboards import keyboard_get_confirm, keyboard_de_unknown_sender, cancel_kb_txt, cancel_kb_media
from core.config import LINK, ADMIN_ID, bot




async def anonim_mes_Command(message: Message, state: FSMContext):
    await message.answer('Введите рефералку получателя Вашего сообщения')
    await state.set_state(SaveSteps.COMMAND_ANONIM_MESSAGE)



async def command_anonim_message(message: Message, state: FSMContext, db: PgSql):
    """Переход при команде 'anonim_message' """
    global text, kb
    link_mes = message.text
    refer = ''
    for i in range(len(link_mes)):
        if link_mes[i].isdigit():
            refer += link_mes[i]
    try:
        ref = int(refer)
        await state.update_data(ref=ref)
    except ValueError:
        text, kb = 'Такой ссылки не существует', ReplyKeyboardRemove()
        await state.clear()
    else:
        hozain = await db.adresat_id(ref)

        if hozain:
            await state.set_state(SaveSteps.GET_UNK_MESSAGE)
            await state.update_data(hozain=hozain[0]['f_name'])
            text, kb = f'✍️Напишите анонимное сообщение пользователю {hozain[0]["f_name"]}', cancel_kb_txt()
    await message.answer(text, reply_markup=kb)


async def anonim_mes_start(message: Message, state: FSMContext, db: PgSql):
    """Если Юзер заходит впервые через Реферальную ссылку"""
    ref = (await state.get_data()).get('ref')
    hozain = await db.adresat_id(ref)

    if hozain:
        await state.set_state(SaveSteps.GET_UNK_MESSAGE)
        await state.update_data(hozain=hozain[0]['f_name'])
        text_, kb_ = f'✍️Напишите анонимное сообщение пользователю {hozain[0]["f_name"]}', cancel_kb_txt()
    else:
        text_, kb_ = 'Такой ссылки не существует', ReplyKeyboardRemove()
        await state.clear()

    await message.answer(text_, reply_markup=kb_)


async def get_message_2(message: Message, state: FSMContext):
    text_ = '📷Можешь прислать до 10 фото или видео'
    kb_ = cancel_kb_media()
    _state = None
    if message.text == 'Отмена❌':
        text_, kb_ = 'Действие отменено', ReplyKeyboardRemove()
        await state.clear()
    elif message.text == "Без текста✏️":
        _state = SaveSteps.MEDIA_HANDLER
        await state.update_data(media=[], seti=set())
    else:
        await state.update_data(unk_mes=message.text, media=[], seti=set())
        _state = SaveSteps.MEDIA_HANDLER

    await message.answer(text_, reply_markup=kb_)
    await state.set_state(state=_state)


async def get_alias(message: Message, state: FSMContext):
    """Получаем Псевдоним отправителя"""
    context_data = await state.get_data()
    text_unk = context_data.get('unk_mes')
    medias = context_data.get('media')
    len_medias = context_data.get('len_medias')
    if not text_unk and not len_medias:
        await message.answer('Нельзя отправить сообщение без фото и текста!', reply_markup=ReplyKeyboardRemove())
        await state.clear()
        return


    alias = 'Неизвестный' if message.text == 'Продолжить без псевдонима😶‍🌫️' else message.text
    await state.update_data(alias=alias)

    hozain = context_data.get('hozain')
    text_ = 'Ваше сообщение: \n\n{}\n\nОт кого: {}\nКому: {}'.format(text_unk or ' ', alias, hozain)
    text_add = '\n\nПодтвердить отправку?'

    await state.update_data(text_mes=text_)


    if medias:
        media_group = media_assembler(medias, text_)
        await message.answer_media_group(media_group.build())
    else:
        await message.answer(text_)

    await state.update_data(mes_id=message.message_id + 1)
    await message.answer(text_add, reply_markup=keyboard_get_confirm())
    await state.set_state(SaveSteps.GET_CONFIRM)


async def get_confirm(message: Message, state: FSMContext, db: PgSql):
    if message.text == 'Подтвердить✅':
        context_data = await state.get_data()
        text_ = context_data.get('unk_mes') or ' '
        medias = context_data.get('media')
        len_medias = context_data.get('len_medias')
        alias = context_data.get('alias')
        hozain = context_data.get('ref')

        mes_for_hozain = f"Вам от ✨ {alias} ✨\n\n{text_}\n\n#полученные"
        try:
            if len_medias:
                media_group = media_assembler(medias, mes_for_hozain)
                await bot.send_media_group(hozain, media_group.build())
                await message.answer('Узнать отправителя👇',
                                     reply_markup=keyboard_de_unknown_sender(message.chat.id))
            else:
                await bot.send_message(hozain, mes_for_hozain, reply_markup=keyboard_de_unknown_sender(message.chat.id))
            await db.sent_receive_Transaction(message.chat.id, hozain)
            await message.answer('Сообщение отправлено!', reply_markup=ReplyKeyboardRemove())

        except Exception as e:
            await bot.send_message(ADMIN_ID, f'<b>{message.chat.id} -> {hozain}</b>\n\n{e}')
            await message.answer('Отправка сообщения не удалась. Скорее всего, Получатель заблокировал бота😢')
        else:
            text_ = context_data.get('text_mes') + '\n#отправленные'

            mes_id = context_data.get('mes_id')

            if len_medias:
                media = InputMediaPhoto(media=medias[0][0], caption=text_)
                if medias[0][1]:
                    media = InputMediaVideo(media=medias[0][0], caption=text_)
                await bot.edit_message_media(chat_id=message.chat.id, message_id=mes_id, media=media)
            else:
                await bot.edit_message_text(chat_id=message.chat.id, message_id=mes_id, text=text_)


        await message.answer('А пока можете разместить свою ссылку, чтобы получать сообщения😉\n'
                             + LINK.format(message.chat.id), reply_markup=ReplyKeyboardRemove())
        await state.clear()

    elif message.text == 'Изменить✏️':

        await anonim_mes_start(message, state, db)

    elif message.text == 'Отмена❌':
        await message.answer('Действие отменено', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
        await state.clear()

    else:
        await message.answer('Неизвестная команда! Вводите команды с клавиатуры\n\nДействие отменено🚫', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))

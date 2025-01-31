import asyncio

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from core.utils.keyboards import opportunity_cancel_nick
from core.utils.state_machine import SaveSteps


async def media_handler(message: Message, state: FSMContext):
    context = await state.get_data()
    seti = context.get('seti')
    photos_videos = context.get('media')

    if message.photo:
        photos_videos.append((message.photo[-1].file_id, 0))
    elif message.video:
        photos_videos.append((message.video.file_id, 1))

    await state.update_data(media=photos_videos)
    await asyncio.sleep(1)

    if message.media_group_id not in seti:
        seti.add(message.media_group_id)
        await state.update_data(seti=seti, len_medias=len(photos_videos))

        await message.answer('Оставь свой псевдоним🥸', reply_markup=opportunity_cancel_nick())
        await state.set_state(SaveSteps.GET_ALIAS)

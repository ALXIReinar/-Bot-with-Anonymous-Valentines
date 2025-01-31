from aiogram import Bot
from aiogram.types import CallbackQuery, PreCheckoutQuery, LabeledPrice

from core.config import PAY_TOKEN, bot
from core.data.postgres import PgSql
from core.utils.keyboards import keyboard_pay, hyper_link_profile


async def pay_window(bot: Bot, call: CallbackQuery):
    anonim_sender = call.data[2:]
    await bot.send_invoice(
        chat_id=call.message.chat.id,
        title='Узнать отправителя сообщения',
        description='После покупки вы получите ссылку на профиль пользователя, отправившего ЭТО анонимное сообщение',
        payload=anonim_sender,
        provider_token=PAY_TOKEN,
        currency='rub',
        max_tip_amount=5000,
        suggested_tip_amounts=[1000, 2000, 3000, 4000],
        start_parameter='pre_reg',
        prices=[
            LabeledPrice(
                label='Доступ к отправителю',
                amount=149_00
            ),
            LabeledPrice(
                label='НДС',
                amount=-2000
            ),
            LabeledPrice(
                label='Скидка',
                amount=-3000
            ),
            LabeledPrice(
                label='Бонус',
                amount=-2000
            )
        ],
        provider_data=None,
        photo_url='https://avatars.mds.yandex.net/i?id=5c57cf011d381fe2800afe7832809edb941df43e-10768430-images-thumbs&n=13',
        photo_size=100,
        photo_width=736,
        photo_height=523,
        need_name=True,
        need_phone_number=False,
        need_email=True,
        need_shipping_address=False,
        send_phone_number_to_provider=False,
        send_email_to_provider=True,
        is_flexible=False,
        disable_notification=False,
        protect_content=False,
        allow_sending_without_reply=False,
        reply_markup=keyboard_pay(f'*_{anonim_sender}'),
        request_timeout=20,
        reply_to_message_id=None,
    )


async def accepting(query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(query.id, ok=True)


async def accept_pay(call: CallbackQuery, db: PgSql):
    """Оплата"""
    tg_id = call.message.chat.id
    anonim_sender = call.data[2:]

    suc_payment = call.message.successful_payment
    if suc_payment:
        """Если деньгами"""
        anonim_sender = suc_payment.invoice_payload
        caption = f'Платёж успешен: {call.message.successful_payment.total_amount // 100}{call.message.successful_payment.currency}\n\n#рассекреченные'

    else:
        """Если Деанонами"""
        if await db.check_balance_deunknown(tg_id):
            await db.debiting_deunknowns(tg_id)
        else:
            await call.message.answer('Недостаточно Деанонов!')
            await call.answer()
            return

        caption = 'Списание успешно!\n\n#рассекреченные'
    await call.message.answer_photo(photo='https://sun1-13.userapi.com/s/v1/ig2/HkdpjdeYsKpEPkTmwgt-wXWEVwpcdbd2VnLH65D0qO0roVKyqZOnRNKPgIcY10A9mSQH5kc21MmPy4VIzOrZgExL.jpg?size=1185x1185&quality=95&crop=247,2,1185,1185&ava=1',
                               caption=caption,
                               reply_markup=hyper_link_profile(anonim_sender, 'Отправитель сообщения😱'))
    await bot.delete_message(tg_id, message_id=call.message.message_id)


from aiogram.fsm.state import StatesGroup, State


class SaveSteps(StatesGroup):
    COMMAND_ANONIM_MESSAGE = State()
    GET_UNK_MESSAGE = State()

    MEDIA_HANDLER = State()
    GET_ALIAS = State()
    GET_CONFIRM = State()


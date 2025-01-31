from aiogram.utils.media_group import MediaGroupBuilder


def media_assembler(file_ids: list,caption=None):
    """Формирует Медиа-Группу для отправки"""
    media_group = MediaGroupBuilder(caption=caption)
    i = 0
    for file_id, identifier in file_ids:
        if i > 9:
            break

        _type = 'photo'
        if identifier:
            _type = 'video'
        media_group.add(type=_type, media=file_id)

        i += 1
    return media_group

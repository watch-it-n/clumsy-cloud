# Don't Remove Credit @letswatchitnow
# Subscribe YouTube Channel For Amazing Bot @letswatchitnow
# Ask Doubt on telegram @letswatchitnow

from pyrogram import Client, filters
from info import CHANNELS
from database.ia_filterdb import save_file
from poppy.util.file_name import append_infinity_to_caption_filename

media_filter = filters.document | filters.video

@Client.on_message(filters.chat(CHANNELS) & media_filter)
async def media(bot, message):
    media = getattr(message, message.media.value, None)
    raw_caption = str(message.caption).strip() if message.caption else ""
    refined_caption = append_infinity_to_caption_filename(raw_caption) if raw_caption else ""
    media.caption = refined_caption or message.caption
    if refined_caption and refined_caption != raw_caption:
        try:
            await message.edit_caption(refined_caption)
        except Exception:
            # Indexing should still work if Telegram does not allow caption edits.
            pass
    await save_file(media)


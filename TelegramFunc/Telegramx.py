from Enums.status_enums import Status
from config import *
import SpotifyFunc.Spotix
import Enums.status_enums
CURRENT_TRACK = None
CURRENT_ALBUM = None
CHANNEL_ID = CFG_CHANNEL_ID
CHANNEL_MESSAGE_ID = CFG_CHANNEL_MESSAGE_ID

async def update_telegram_post(bot: Bot, playback_info, cover_path, status) -> None:
    global CHANNEL_ID, CHANNEL_MESSAGE_ID, CURRENT_TRACK
    if status == Status.PLAYING:
        track = playback_info["item"]
        artist_names = ', '.join([artist['name'] for artist in track['artists']])
        if track['id'] == CURRENT_TRACK:
            return

        SpotifyFunc.Spotix.download_album_cover(playback_info, current_album_info=track['album']['name'])

        caption_text = (
            f"<b>СЕЙЧАС ИГРАЕТ</b>\n"
            f"\n"
            f"<blockquote>"
            f"<b>Трек:</b> {track['name']}\n"
            f"<b>Исполнитель(и):</b> {artist_names}\n"
            f"<b>Альбом:</b> {track['album']['name']}"
            f"</blockquote>\n"
            f"\n<a href='{track['external_urls']['spotify']}'>Слушать на Spotify</a>"
        )

        if status == 1:
            caption_text = ("<b>PAUSED</b>\n\n" + caption_text)

        cover_photo = FSInputFile(cover_path)

        try:
            if CHANNEL_MESSAGE_ID:
                media = InputMediaPhoto(media=cover_photo, caption=caption_text, parse_mode=ParseMode.HTML)

                sent_message = await bot.edit_message_media(
                    chat_id=CHANNEL_ID,
                    message_id=CHANNEL_MESSAGE_ID,
                    media=media
                )

                CHANNEL_MESSAGE_ID = sent_message.message_id
                CURRENT_TRACK = track['id']
                print(f'[TELEGRAM] Post succesfully changed: {sent_message.message_id}')
            else:
                print("[TELEGRAM] Post not found")
        except Exception as e:
            print(e)
    else:
        cover_photo = FSInputFile("Images/black.jpg")
        caption_text = ("...")
        media = InputMediaPhoto(media=cover_photo, caption=caption_text, parse_mode=ParseMode.HTML)
        sent_message = await bot.edit_message_media(
            chat_id=CHANNEL_ID,
            message_id=CHANNEL_MESSAGE_ID,
            media=media
        )
        CHANNEL_MESSAGE_ID = sent_message.message_id
        CURRENT_TRACK = None
        print(f'[TELEGRAM] Spotify disabled: {sent_message.message_id}')





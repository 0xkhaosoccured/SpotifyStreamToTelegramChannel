from Enums.status_enums import Status
from config import *
import Enums.status_enums
from TelegramFunc.Telegramx import update_telegram_post

CURRENT_ALBUM = None

def download_album_cover(playbackinfo, current_album_info) -> None:
    global CURRENT_ALBUM
    track = playbackinfo['item']
    if current_album_info == CURRENT_ALBUM:
        print("Album cover already downloaded")
        return
    album_image_link = track['album']['images'][0]['url']
    if not os.path.exists("Images"):
        Path("Images/AlbumCovers").mkdir(parents=True, exist_ok=True)
    response = requests.get(album_image_link)
    filepath = 'Images/AlbumCovers/AlbumCover.jpg'
    if response.status_code == 200:
        with open(filepath, 'wb') as f:
            f.write(response.content)
        CURRENT_ALBUM = current_album_info
        print(f"{album_image_link} downloaded")
    else:
        print(f"unable to download {album_image_link}")

async def spotifyMonitor(spotify_obj, bot) -> None:
    try:
        while True:
            await asyncio.sleep(TIMER_C)
            playback_info = spotify_obj.current_playback()
            if playback_info and playback_info['is_playing']:
                print("[PLAYING]")
                await update_telegram_post(bot, playback_info, "Images/AlbumCovers/AlbumCover.jpg", status=Status.PLAYING)
            elif playback_info and not playback_info['is_playing']:
                print("[PAUSED]")
                pass
            else:
                print("[STOPPED]")
                await update_telegram_post(bot, playback_info, "Images/AlbumCovers/AlbumCover.jpg", status=Status.STOPPED)

    except Exception as e:
        print("Error inside [SPOTIFYMONITOR] function: " + str(e))
        await asyncio.sleep(5)
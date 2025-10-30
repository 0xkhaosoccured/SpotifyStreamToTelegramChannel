from config import *
import SpotifyFunc.Spotix

dp = Dispatcher()

async def main() -> None:
    spotify_task = asyncio.create_task(SpotifyFunc.Spotix.spotifyMonitor(spotify_obj=spotify, bot=bot))
    try:
        await dp.start_polling(bot)
    finally:
        spotify_task.cancel()
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

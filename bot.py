import asyncio
import os
import yt_dlp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile

API_TOKEN = os.getenv("BOT_TOKEN")
print("TOKEN LOADED:", bool(API_TOKEN), API_TOKEN[:10] if API_TOKEN else None)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def download_video(url):
    ydl_opts = {
        "format": "bv*+ba/b",
        "merge_output_format": "mp4",
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "noplaylist": True,
        "quiet": False,
        "cookiefile": "cookies.txt",  
        "postprocessors": [{
            "key": "FFmpegVideoConvertor",
            "preferedformat": "mp4",
}],
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.tiktok.com/",
        },
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "أرسل رابط TikTok أو Instagram أو Twitter(X) وسأحاول تحميله لك."
    )

@dp.message(
    F.text.contains("tiktok.com") |
    F.text.contains("instagram.com") |
    F.text.contains("x.com") |
    F.text.contains("twitter.com")
)
async def handle_video(message: types.Message):

    try:
        path = await asyncio.to_thread(download_video, message.text)
        await message.answer_video(video=FSInputFile(path))
        os.remove(path)
        await message.delete()
    except Exception as e:
        await message.answer(f"❌ خطأ: {e}")

async def main():
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

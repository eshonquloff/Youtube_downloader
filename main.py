import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.bot import base
from dotenv import load_dotenv
from pytube import YouTube

load_dotenv()

api_token = os.getenv('BOT_TOKEN')


bot = Bot(token=api_token)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def greet_fun(msg: types.Message):
    await bot.send_message(msg.chat.id, "Send me Youtube video link..")


@dp.message_handler()
async def video_get(msg: types.Message):
    link = msg.text
    if link.startswith('http'):
        await bot.send_message(msg.chat.id, 'Downloading this video...')
        from io import BytesIO
        buffer = BytesIO()
        url = YouTube(link)
        if url.check_availability() is None:
            video = url.streams.get_audio_only()
            video.stream_to_buffer(buffer=buffer)
            buffer.seek(0)
            title = url.title
            await bot.send_video(msg.chat.id, video=buffer, caption=title, thumb=f'{url.thumbnail_url}')
        await bot.send_message(msg.chat.id, 'Video is successfully downloaded! ✅')
    else:
        await bot.send_message(msg.chat.id, 'Oops! Invalid link🤥')


async def on_startup(dispatcher, url=None, cerf=None):
    print('Bot turned on.')


async def on_shutdown(dispatcher):
    print('Bot turned off.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)

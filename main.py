import os
from aiogram import Bot, Dispatcher, executor, types
from func import download_video
from dotenv import load_dotenv

load_dotenv()

api_token = os.getenv('BOT_TOKEN')


bot = Bot(token=api_token)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def greet_fun(msg: types.Message):
    await bot.send_message(msg.chat.id, "Send me Youtube video link..")


@dp.message_handler()
async def video_get(msg: types.Message):
    if msg.text.startswith('https://www.youtube.com/') or msg.text.startswith('https://youtu.be/'):
        await bot.send_message(msg.chat.id, 'Downloading this video...')
        video = download_video(msg.text)
        with open(f'videos/{video.title}.{video.subtype}', 'rb') as f:
            await bot.send_video(msg.chat.id, video=f, caption=f'{video.title}')
        await bot.send_message(msg.chat.id, 'Video is successfully downloaded! ✅')
        os.remove(f'videos/{video.title}.{video.subtype}')
    else:
        await bot.send_message(msg.chat.id, 'Oops! Invalid link🤥')


async def on_startup(dispatcher, url=None, cerf=None):
    print('Bot turned on.')


async def on_shutdown(dispatcher):
    print('Bot turned off.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)

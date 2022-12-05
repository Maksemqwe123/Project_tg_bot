from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import BOT_TOKEN

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

if __name__ == '__main__':
    from handler import dp
    executor.start_polling(dp, skip_updates=True)

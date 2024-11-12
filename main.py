from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from cfg import TOKEN

from indushka import get_recs, get_TA, make_table

# All handlers should be attached to the Router (or Dispatcher)
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=["start"])
async def start(message: types.Message) -> None:
    await message.reply('Хочешь заклюю?')


@dp.message_handler(commands=["help"])
async def start(message: types.Message) -> None:
    await message.reply("Отправь криптопару для получения рекомендации.\n"
                        "Пример: btc 1d bybit, pepebtc 4h.\n"
                        "По умолчанию биржа MEXC.")


@dp.message_handler(commands=["sent"])
async def start(message: types.Message) -> None:
    await message.answer('<pre>' + make_table(get_recs()) + '</pre>', parse_mode='html')


@dp.message_handler()
async def parse_and_reply(message: types.Message) -> None:
    request = message.text.split(' ')
    result = get_TA(*request)

    if result is None:
        await message.answer(f"<a href='https://www.tradingview.com/chart/?symbol={request[0].upper()}'>Биржа или "
                             f"криптопара не найдена.</a>", parse_mode='html')
        return
    else:
        await message.answer('<pre>' + result + '</pre>', parse_mode='html')


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)

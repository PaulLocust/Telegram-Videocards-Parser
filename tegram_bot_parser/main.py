import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, utils, types
from aiogram.types import ParseMode
from config import TOKEN, URL
from db import process_search_model, init_db, find_id_search, find_all_cards
from parser import ParseVideoCard

logging.basicConfig(level=logging.INFO)

# -----CREATING BOT-----
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)

# -----CREATING DISPATCHER-----
dp = Dispatcher(bot)


# -----START and HELP-----
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm ParseBot!\nFucking Fuck!")


# -----SENDING LIST OF STRINGS-----
@dp.message_handler(commands='list')
async def send_list(message: types.Message):
    search_models = find_id_search(message.chat.id)
    cards = find_all_cards()
    for card in cards:
        card_title = card.title
        for model in search_models:
            search_title = model.title
            if card_title.find(search_title) >= 0:
                message_text = 'Строка поиска {} \r\n Найдено {}'.format(search_title, utils.markdown.hlink(card_title, card.url))
                await message.answer(text=message_text, parse_mode=ParseMode.HTML)


# -----SENDING LIST OF WORDS-----
@dp.message_handler(commands='search')
async def send_search(message: types.Message):
    search_models = find_id_search(message.chat.id)
    for model in search_models:
        await message.answer(text=model.title)


# -----SAVING OR DELETING MODELS-----
@dp.message_handler()
async def echo(message: types.Message):
    await process_search_model(message)


# -----WAITING AND PARSING-----
async def scheduled(wait_for, parser):
    while True:
        await asyncio.sleep(wait_for)
        await parser.parse()


# -----RUNNING OUR SCRIPT-----
if __name__ == "__main__":
    init_db()
    parser = ParseVideoCard(url=URL, bot=bot)
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(30, parser))

    # Запуск бота
    executor.start_polling(dp, skip_updates=True)

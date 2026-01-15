import random
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram.filters import Command

# Вставь свой токен (лучше через переменную окружения BOT_TOKEN)
BOT_TOKEN = os.getenv("BOT_TOKEN", "8315575890:AAEumIJmQ3Wg4X0HnH3CX8O7apeHKqox0Io")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
END_GIF_URL = os.getenv("END_GIF_URL", "https://media.tenor.com/JTq6kYdZlZ0AAAAd/the-end.gif")
END_GIF_FILE_ID = os.getenv("END_GIF_FILE_ID", "CgACAgQAAxkBAAN-aN5ez5cuR09Ebc65-tV__WXD3CcAAjkEAAL_vK1SuacF9FStzRM2BA")

# Фразы для каждого человека
phrases = {
    "Данил": ['никит, девочку то нашел в москве своей', 'говно ваш морген', 'да я щас вас разъебу', 'еду кефту хавать', 'бля ебать бидоны у анетты', 'сука опять на афган идти', 'кэмбридж хуйня, А ВОТ ОГЭ...', 'идем искать четсер стронг','сопельки у бедненького мальчика', 'да бля какие дворики', 'штро?', 'вкусность ебаная'],
    "Дима": ['теперь ты профессор', 'алё на хуй иди', 'сомелье хуев', 'да я кхм кхм её', 'я в голландию к ней поеду', 'сын моргенштерна', 'заебал со своей офф', 'дмитрий алексеевич шалава', 'на фб к душечкиной', 'харри магвая', 'пьяный иван зоммер', 'боб строитель', 'я в ссылке', 'че за апчхуй приехал, где s-класс?', 'какое нахуй такси, идем пешком'],
    "Никита": [' Что такое Зимний дворец? Зимний дворец — это один из самых известных музеев, картинных галерей во всей России. Также люди знают его не как Зимний дворец, а как Эрмитаж. Давайте разберемся с вами, что такое Эрмитаж. Эрмитаж, если углубиться в его значение, означает место уединения. Так давайте выпьем за то, что наша дача станет нашим Эрмитажем.  s', 'ударяй', 'за нас с нами и за хуй с ними', 'жигуль', 'профессор', 'бездарь', 'шалава из ранхигса', 'ты думал будет гол- наебал; я - ударяйка, подпишись на анал', 'костяной', 'у языка 2 функции: пиздеть и лизать. какая из них мужская, какая женская, додумаешь сам', 'каждому по три', 'ИИУУУУУ', 'Вертушку давно не получал?', 'Рубрика: туалетные истории', 'Вы чё, все пизды хотите получить', 'хочу трахать каждую из чикс лайф', 'я сосу и трахаю']
}

# Храним прогресс пользователя
progress = {}

# Приветственное сообщение и выбор имени
@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text="Данил", callback_data="choose_Данил")],
        [types.InlineKeyboardButton(text="Дима", callback_data="choose_Дима")],
        [types.InlineKeyboardButton(text="Никита", callback_data="choose_Никита")]
    ]
    )
    await message.answer('Привет! Тут живут трое гениев, плейбоев, миллиардеров, филантропов: Данил, Дима, Никита')
    await message.answer("Выбери пидора:", reply_markup=keyboard)


# Выбор имени
@dp.callback_query(F.data.startswith("choose_"))
async def choose_name(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    name = callback.data.split("_")[1]

    shuffled = phrases[name][:]
    random.shuffle(shuffled)

    progress[user_id] = {"name": name, "remaining": shuffled}
    await send_phrase(callback.message, user_id)
    await callback.answer()


# Отправка фразы
async def send_phrase(message, user_id):
    data = progress[user_id]
    name = data["name"]
    remaining = data["remaining"]

    if not remaining:
        keyboard = types.InlineKeyboardMarkup(
            inline_keyboard=[[types.InlineKeyboardButton(text="Хочу другого пидора", callback_data="change")]]
        )
        end_animation = END_GIF_FILE_ID if END_GIF_FILE_ID else END_GIF_URL
        await message.answer_animation(
            animation=end_animation,
            caption=f"{name} больше не может ниче пиздануть. Выбери другого хуесоса",
            reply_markup=keyboard,
        )
        return

    phrase = remaining.pop(0)
    is_now_empty = not remaining
    buttons = []
    if not is_now_empty:
        buttons.append([types.InlineKeyboardButton(text="Аххх ещеее", callback_data="next")])
    buttons.append([types.InlineKeyboardButton(text="Хочу другого пидора", callback_data="change")])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(phrase, reply_markup=keyboard)
    if is_now_empty:
        end_animation = END_GIF_FILE_ID if END_GIF_FILE_ID else END_GIF_URL
        await message.answer_animation(
            animation=end_animation,
            caption=f"{name} больше не может ниче пиздануть. Выбери другого хуесоса",
        )


# Продолжить фразы
@dp.callback_query(F.data == "next")
async def next_phrase(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in progress:
        await callback.message.answer("Сначала выбери имя гандона через /start")
    else:
        await send_phrase(callback.message, user_id)
    await callback.answer()


# Сменить имя
@dp.callback_query(F.data == "change")
async def change_name(callback: types.CallbackQuery):
    await start(callback.message)
    await callback.answer()


# Вспомогательный хендлер: пришли боту GIF, чтобы получить его file_id
@dp.message(F.animation)
async def get_animation_file_id(message: types.Message):
    file_id = message.animation.file_id
    await message.answer(f"file_id: {file_id}")


# Запуск бота
async def main():
    if not BOT_TOKEN:
        raise RuntimeError("Не задан BOT_TOKEN в переменных окружения")
    # На всякий случай убираем webhook, если он был установлен, чтобы избежать 409-конфликта
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

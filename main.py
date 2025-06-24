import os
import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_LINK = "https://t.me/bbsignalss"
CHANNEL_USERNAME = "@bbsignalss"
REF_LINK = "https://1whecs.life/v3/lucky-jet-updated?p=hee9"

TEXT = {
    "ru": {
        "choose_lang": "🌐 *Выберите язык* 🇷🇺 / 🇺🇦",
        "lang_ru": "Русский 🇷🇺",
        "lang_ua": "Українська 🇺🇦",
        "start": (
            "🔥 *ТЕ, КТО ИДУТ ПРОТИВ ПРАВИЛ, ВСЕГДА В ВЫИГРЫШЕ\\. ПОРА СЫГРАТЬ ПО\\-ТВОЕМУ\\!* \n\n"
            "🤖 _LuckyJet Сигналы — твой шанс на плюс_\\! \n\n"
            "Наш бот подключён к *уникальному ИИ*, который анализирует скрытые алгоритмы Lucky Jet и вычисляет следующие иксы до начала раунда\\. \n\n"
            "🟢 *Точность сигналов — до 90%*\\! \n"
            "🛡️ Всё абсолютно легально — используем открытые статистические лазейки, которые до сих пор не прикрыли разработчики\\. \n\n"
            "_\\(В первые минуты ИИ тестирует твою сессию, чтобы понять паттерн аккаунта\\. С каждой игрой точность сигналов только растёт\\!\\)_"
        ),
        "subscribe": "🎯 *Чтобы получить доступ к сигналам, подпишись на наш канал*:",
        "go_to_channel": "🔗 Перейти в канал",
        "check_sub": "✅ Проверить подписку",
        "not_sub": "❗️ *Вы не подписаны на канал*\\. \n\nПожалуйста, подпишитесь и попробуйте снова\\.",
        "deposit_request": (
            "💸 *Чтобы бот начал работу, внеси депозит на 1Win\\!* \n\n"
            "⚖️ _Оптимальный диапазон депозита — от 1000₴ до 10 000₴\\._\n"
            "Мелкие депы не советуем: *алгоритмы режут крупные коэффициенты для маленьких ставок\\.*\n"
            "Но и жадничать не нужно — суммы больше 10 000₴ могут привлечь внимание службы безопасности казино\\.\n\n"
            "💡 *По опыту “старичков”*: кто стартует в этом диапазоне, уже на первых раундах ловит хорошие иксы и не попадает в “риск\\-группу”\\.\n\n"
            "📲 *Пришли сюда скриншот своего депозита* — обработка займёт меньше минуты, твои данные защищены\\!"
        ),
        "wait_deposit": (
            "🕒 *Проверяем депозит*\\.\n"
            "Подожди буквально 10 секунд — идёт анализ сессии ИИ\\!"
        ),
        "access": (
            "🎉 *Поздравляем\\!* Ты всё сделал правильно — доступ к сигналам Lucky Jet открыт\\!\n\n"
            "🚀 *Желаем мощных иксов и только крупных побед\\!* \n\n"
            "Нажимай кнопку ниже, чтобы получить свой первый сигнал\\. ⬇️"
        ),
        "signal_btn": "🎰 Получить сигнал",
        "wait_signal_btn": "⏳ Ожидайте\\.\\.\\.",
        "analyzing": "🤖 ИИ собирает свежие данные по коэффициентам\\.\n⏳ Ожидайте \\- это займёт пару секунд\\.",
        "get_signal": "🎯 *Лови коэффициент*: x{:.2f}",
        "reviews": "📢 Отзывы",
        "back": "⬅️ Назад",
        "registered": "✅ Зарегистрировался"
    }
}

USERS = {}

bot = Bot(token=BOT_TOKEN, parse_mode="MarkdownV2")
dp = Dispatcher(bot)

# --- PROGRESS BAR ФУНКЦИЯ ---
async def show_progress_bar(chat_id):
    bars = [
        "🕒 ▒▒▒▒▒▒▒▒▒▒ 0%",
        "🕒 ███▒▒▒▒▒▒▒ 30%",
        "🕒 ██████▒▒▒▒ 60%",
        "🕒 ██████████ 100%",
    ]
    msg = await bot.send_message(chat_id, bars[0])
    for i in range(1, len(bars)):
        await asyncio.sleep(0.7)
        await bot.edit_message_text(bars[i], chat_id, msg.message_id)
    await asyncio.sleep(0.5)
    await bot.delete_message(chat_id, msg.message_id)

def lang_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(TEXT["ru"]["lang_ru"], TEXT["ru"]["lang_ua"])
    return kb

def channel_and_check_kb():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(TEXT["ru"]["go_to_channel"], url=CHANNEL_LINK),
        InlineKeyboardButton(TEXT["ru"]["check_sub"], callback_data="check_sub")
    )
    return kb

def after_sub_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton(TEXT["ru"]["back"], callback_data="back_to_sub"),
        InlineKeyboardButton(TEXT["ru"]["registered"], callback_data="registered")
    )
    return kb

def after_sub_text():
    return (
        "🥇 *Отлично\\!*\n\n"
        "Теперь твой следующий шаг \\- регистрация на 1Win\\. Только так ИИ сможет “видеть” твои раунды и давать сигналы\\.\n\n"
        "💸 Регистрируйся только по этой [Перейти к регистрации]({}) \\(даже если у тебя уже есть аккаунт \\- просто создай новый\\!\\)\\.\n"
        "_Если регистрация будет не по этой ссылке \\- скрипт не сработает и сигналы не будут актуальными\\._"
    ).format(REF_LINK)

def deposit_kb():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(TEXT["ru"]["reviews"], url=CHANNEL_LINK),
        InlineKeyboardButton(TEXT["ru"]["back"], callback_data="back_to_register")
    )
    return kb

def signal_kb(active=True):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    if active:
        kb.add(TEXT["ru"]["signal_btn"], TEXT["ru"]["back"])
    else:
        kb.add(TEXT["ru"]["wait_signal_btn"], TEXT["ru"]["back"])
    return kb

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    USERS[message.from_user.id] = {
        "step": "choose_lang",
        "signals_given": 0,
        "access": False,
        "can_signal": True
    }
    await message.answer(TEXT["ru"]["choose_lang"], reply_markup=lang_kb())

@dp.message_handler(lambda m: m.text in [TEXT["ru"]["lang_ru"], TEXT["ru"]["lang_ua"]])
async def choose_lang(message: types.Message):
    USERS[message.from_user.id]["step"] = "start"
    await message.answer(TEXT["ru"]["start"], reply_markup=types.ReplyKeyboardRemove())
    await message.answer(
        TEXT["ru"]["subscribe"],
        reply_markup=channel_and_check_kb()
    )

@dp.callback_query_handler(lambda call: call.data == "check_sub")
async def check_sub(call: types.CallbackQuery):
    USERS[call.from_user.id]["step"] = "register"
    await call.message.answer(after_sub_text(), reply_markup=after_sub_kb())

@dp.callback_query_handler(lambda call: call.data == "back_to_sub")
async def back_to_sub(call: types.CallbackQuery):
    USERS[call.from_user.id]["step"] = "start"
    await call.message.answer(TEXT["ru"]["subscribe"], reply_markup=channel_and_check_kb())

@dp.callback_query_handler(lambda call: call.data == "back_to_register")
async def back_to_register(call: types.CallbackQuery):
    USERS[call.from_user.id]["step"] = "register"
    await call.message.answer(after_sub_text(), reply_markup=after_sub_kb())

@dp.callback_query_handler(lambda call: call.data == "registered")
async def registered_step(call: types.CallbackQuery):
    USERS[call.from_user.id]["step"] = "deposit"
    await call.message.answer(TEXT["ru"]["deposit_request"], reply_markup=deposit_kb())

@dp.message_handler(lambda m: USERS.get(m.from_user.id, {}).get("step") == "deposit" and m.text == TEXT["ru"]["back"])
async def back_to_deposit(message: types.Message):
    USERS[message.from_user.id]["step"] = "register"
    await message.answer(after_sub_text(), reply_markup=after_sub_kb())

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def deposit_check(message: types.Message):
    user = USERS.get(message.from_user.id)
    if user and user.get("step") == "deposit":
        USERS[message.from_user.id]["step"] = "wait"
        await message.answer(TEXT["ru"]["wait_deposit"])
        await asyncio.sleep(10)
        USERS[message.from_user.id]["access"] = True
        USERS[message.from_user.id]["step"] = "signals"
        USERS[message.from_user.id]["can_signal"] = True
        await message.answer(TEXT["ru"]["access"], reply_markup=signal_kb())

@dp.message_handler(lambda m: USERS.get(m.from_user.id, {}).get("step") == "signals" and m.text == TEXT["ru"]["back"])
async def back_to_signals(message: types.Message):
    USERS[message.from_user.id]["step"] = "deposit"
    await message.answer(TEXT["ru"]["deposit_request"], reply_markup=deposit_kb())

# --- ВЫДАЧА СИГНАЛА С PROGRESS BAR ---
@dp.message_handler(lambda m: m.text == TEXT["ru"]["signal_btn"])
async def send_signal(message: types.Message):
    user = USERS.get(message.from_user.id)
    if not user or not user.get("access") or not user.get("can_signal"):
        return
    USERS[message.from_user.id]["can_signal"] = False

    await message.answer(TEXT["ru"]["analyzing"])
    await asyncio.sleep(5)

    num = user.get("signals_given", 0)
    if num < 3:
        k = round(random.uniform(1.00, 2.00), 2)
    else:
        k = round(random.uniform(2.00, 13.00), 2)

    # Экранируем точку для MarkdownV2!
    k_str = str(k).replace('.', '\\.')
    signal_text = f"🎯 *Лови коэффициент*: x{k_str}"

    await message.answer(signal_text)

    # Показываем прогресс-бар после сигнала
    await show_progress_bar(message.chat.id)

    USERS[message.from_user.id]["signals_given"] = num + 1

    await message.answer(TEXT["ru"]["wait_signal_btn"], reply_markup=signal_kb(active=False))
    await asyncio.sleep(5)
    USERS[message.from_user.id]["can_signal"] = True
    await message.answer("🔁 Можно снова получить сигнал\\!", reply_markup=signal_kb(active=True))

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
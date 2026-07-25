from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import re


# ВСТАВЬТЕ НОВЫЙ ТОКЕН ОТ @BotFather
TOKEN = "8800908083:AAG6nL7rslOpXk6E89EV0JMOTCK974oVHdI"


# Кнопки главного меню
keyboard = [
    ["🇨🇳 Китай"],
    ["🇰🇷 Корея"],
    ["🇯🇵 Япония"],
    ["🏠 Главное меню"],
]


reply_markup = ReplyKeyboardMarkup(
    keyboard,
    resize_keyboard=True,
    one_time_keyboard=False,
)


# Хранилище заявок
user_data = {}


# ID менеджера (можно добавить позже)
MANAGER_CHAT_ID = -5583958583



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚗 Компания «ЧАЙНАОН» приветствует Вас!\n\n"
        "Мы занимаемся доставкой автомобилей ведущих мировых автопроизводителей "
        "из Европы и Азии.\n\n"
        "Пожалуйста, выберите из списка страну, где хотите приобрести автомобиль:",
        reply_markup=reply_markup,
    )



async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    chat_id = update.message.chat.id


    # Выбор страны
    if text in [
        "🇨🇳 Китай",
        "🇰🇷 Корея",
        "🇯🇵 Япония"
    ]:

        user_data[chat_id] = {
            "country": text
        }

        await update.message.reply_text(
            "🚗 Напишите марку и модель автомобиля, если уже знаете, какой автомобиль Вам нужен.\n\n"
            "Например:\n"
            "Toyota Camry 2022\n\n"
            "Если пока не определились — напишите ваши пожелания."
        )

        return


    # Возврат в меню
    if text == "🏠 Главное меню":
        await start(update, context)
        return


    # Если пользователь не начал заявку
    if chat_id not in user_data:
        await update.message.reply_text(
            "Пожалуйста, сначала выберите страну автомобиля:",
            reply_markup=reply_markup,
        )
        return
            # Получение данных анкеты

    if "car_model" not in user_data[chat_id]:

        user_data[chat_id]["car_model"] = text

        await update.message.reply_text(
            "💰 Какой бюджет Вы планируете выделить на покупку автомобиля?"
            
        )

        return



    if "budget" not in user_data[chat_id]:

        user_data[chat_id]["budget"] = text

        await update.message.reply_text(
            "🏙 Укажите Ваш город:"
        )

        return



    if "city" not in user_data[chat_id]:

        user_data[chat_id]["city"] = text

        await update.message.reply_text(
            "👤 Пожалуйста, укажите Ваше имя:"
        )

        return



    if "name" not in user_data[chat_id]:

        user_data[chat_id]["name"] = text

        await update.message.reply_text(
            "📞 Пожалуйста, укажите Ваш номер телефона в формате для \n\n"
            "РФ 7ХХХХХХ\n"
            "РБ 3ХХХХХХ\n\n"
            "Номер нужен для авторизации, проверка защиты от ботов, юлагодарим за понимание."
        )

        return



    if "phone" not in user_data[chat_id]:

        # Проверка телефона
        phone = re.sub(r"\D", "", text)


        if len(phone) < 10:

            await update.message.reply_text(
                "❌ Неверный номер телефона.\n"
                "Введите номер ещё раз."
            )

            return


        user_data[chat_id]["phone"] = text


        # Формирование заявки
        data = user_data[chat_id]


        application_text = (
            "🚗 НОВАЯ ЗАЯВКА\n\n"
            f"🌍 Страна: {data['country']}\n"
            f"🚘 Автомобиль: {data['car_model']}\n"
            f"💰 Бюджет: {data['budget']}\n"
            f"🏙 Город: {data['city']}\n"
            f"👤 Имя: {data['name']}\n"
            f"📞 Телефон: {data['phone']}\n\n"
            f"🆔 Telegram ID: {chat_id}"
        )

        # Отправка заявки в чат менеджеров
        await context.bot.send_message(
            chat_id=MANAGER_CHAT_ID,
            text=application_text
        )

        print(application_text)

        await update.message.reply_text(
            "✅ Ваша заявка принята!\n\n"
            "Наш менеджер свяжется с Вами в ближайшее время.",
            reply_markup=reply_markup,
        )

        # Удаляем данные после завершения
        del user_data[chat_id]

        return


def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            buttons
        )
    )

    print("🤖 Бот запущен...")

    app.run_polling()


if __name__ == "__main__":
    main()
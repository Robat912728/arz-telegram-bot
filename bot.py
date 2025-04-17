
import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8056932706:AAEuhSSCSY8jFOXlHuUzBUfsiPq_w_kSTiE"

URLS = {
    "dollar": "https://api.tgju.org/v1/price/latest/slider",
    "gold": "https://api.tgju.org/v1/price/latest/slider",
    "derham": "https://api.tgju.org/v1/price/latest/slider",
    "coin": "https://api.tgju.org/v1/price/latest/slider"
}

MAPPINGS = {
    "dollar": "price_dollar_rl",
    "gold": "geram18",
    "derham": "price_derham",
    "coin": "sekebahar"
}

def get_price(key):
    try:
        res = requests.get(URLS[key], timeout=10).json()
        price = res['data'][MAPPINGS[key]]['p']
        return f"{key.capitalize()} rate: {price} تومان"
    except Exception as e:
        return f"خطا در دریافت قیمت {key}: {e}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("دلار", callback_data='dollar')],
        [InlineKeyboardButton("درهم", callback_data='derham')],
        [InlineKeyboardButton("طلا", callback_data='gold')],
        [InlineKeyboardButton("سکه", callback_data='coin')],
        [InlineKeyboardButton("همه", callback_data='all')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("یکی از گزینه‌ها رو انتخاب کن:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    choice = query.data
    if choice == "all":
        result = "
".join([get_price(k) for k in MAPPINGS])
    else:
        result = get_price(choice)
    await query.edit_message_text(result)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("all", lambda u, c: u.message.reply_text(
        "
".join([get_price(k) for k in MAPPINGS])
    )))
    app.add_handler(CommandHandler("dollar", lambda u, c: u.message.reply_text(get_price("dollar"))))
    app.add_handler(CommandHandler("derham", lambda u, c: u.message.reply_text(get_price("derham"))))
    app.add_handler(CommandHandler("gold", lambda u, c: u.message.reply_text(get_price("gold"))))
    app.add_handler(CommandHandler("coin", lambda u, c: u.message.reply_text(get_price("coin"))))
    app.run_polling()

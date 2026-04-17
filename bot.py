import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

WALLET_ADDRESS = "TTD267vkgzaDy4PXJ1hyJ3LHVyZSrt81e6"
NETWORK = "TRC20"

packages = {
    "p1": ("5 Credits", 8),
    "p2": ("10 Credits", 15),
    "p3": ("20 Credits", 25),
    "p4": ("30 Credits", 34),
    "p5": ("50 Credits", 50),
    "p6": ("100 Credits", 91),
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("5 Credit cards - $8", callback_data="p1")],
        [InlineKeyboardButton("10 Credit cards - $15", callback_data="p2")],
        [InlineKeyboardButton("20 Credit cards - $25", callback_data="p3")],
        [InlineKeyboardButton("30 Credit cards - $34", callback_data="p4")],
        [InlineKeyboardButton("50 Credit cards - $50", callback_data="p5")],
        [InlineKeyboardButton("100 Credit cards - $91", callback_data="p6")],
    ]

    await update.message.reply_text(
        "💰 Welcome to Hubtel Bot\n\nChoose a package:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_package(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    name, price = packages[query.data]

    keyboard = [
        [InlineKeyboardButton("✅ I Have Paid", callback_data="paid")]
    ]

    await query.message.reply_text(
        f"🛒 {name}\n"
        f"💵 Price: ${price}\n\n"
        f"💳 Send USDT (TRC20 ONLY)\n\n"
        f"📍 Wallet:\n{WALLET_ADDRESS}\n\n"
        f"⚠️ Network: {NETWORK}\n\n"
        f"After payment click below:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "⏳ Payment submitted.\nPlease wait for confirmation."
    )

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_package, pattern="^p"))
app.add_handler(CallbackQueryHandler(confirm, pattern="^paid"))

import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

def run_dummy_server():
    server = HTTPServer(("0.0.0.0", 10000), BaseHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server).start()

app.run_polling()

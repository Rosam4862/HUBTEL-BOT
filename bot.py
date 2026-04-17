import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# =========================
# BOT SETTINGS
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")

WALLET_ADDRESS = "TTD267vkgzaDy4PXJ1hyJ3LHVyZSrt81e6"
NETWORK = "TRC20"

# =========================
# PACKAGES
# =========================

packages = {
    "p1": {"name": "5 Credits", "price": 8},
    "p2": {"name": "10 Credits", "price": 15},
    "p3": {"name": "20 Credits", "price": 25},
    "p4": {"name": "30 Credits", "price": 34},
    "p5": {"name": "50 Credits", "price": 50},
    "p6": {"name": "100 Credits", "price": 91},
}

# =========================
# START COMMAND
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("5 Credits - $8", callback_data="p1")],
        [InlineKeyboardButton("10 Credits - $15", callback_data="p2")],
        [InlineKeyboardButton("20 Credits - $25", callback_data="p3")],
        [InlineKeyboardButton("30 Credits - $34", callback_data="p4")],
        [InlineKeyboardButton("50 Credits - $50", callback_data="p5")],
        [InlineKeyboardButton("100 Credits - $91", callback_data="p6")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "💰 Welcome to Hubtel Bot 💰\n\n"
        "Choose a package below:",
        reply_markup=reply_markup
    )

# =========================
# PACKAGE SELECTED
# =========================

async def handle_package(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    package = packages[query.data]

    keyboard = [
        [InlineKeyboardButton("✅ I Have Paid", callback_data=f"paid_{query.data}")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(
        f"🛒 {package['name']}\n"
        f"💵 Amount: ${package['price']}\n\n"
        f"💳 Send USDT using {NETWORK} Network only\n\n"
        f"📍 Wallet Address:\n{WALLET_ADDRESS}\n\n"
        f"⚠️ Do NOT send on ERC20 or BEP20\n\n"
        f"After payment click ✅ I Have Paid",
        reply_markup=reply_markup
    )

# =========================
# PAYMENT BUTTON CLICKED
# =========================

async def confirm_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "⏳ Payment request received.\n\n"
        "Please wait while your payment is reviewed."
    )

# =========================
# MAIN BOT
# =========================

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_package, pattern="^p"))
app.add_handler(CallbackQueryHandler(confirm_payment, pattern="^paid_"))

print("Hubtel Bot is running...")

app.run_polling()

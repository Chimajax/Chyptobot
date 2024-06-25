from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
    Update,
    WebAppInfo
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters
)
import os

# Your bot token
TOKEN = '6478165635:AAF0XtrVbQb8YptnY3jkIprdfMOwHOYcdCA'

# States for conversation handler
ASK_USERNAME = 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    # Initial message with social media buttons
    buttons = [
        [InlineKeyboardButton("Subscribe to Youtube", url="https://www.youtube.com/@Chypto")],
        [InlineKeyboardButton("Follow our X", url="https://X.com/@Chypto_Official")]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await context.bot.send_message(
        chat_id=chat_id,
        text="Welcome to Chypto\n\nTap, Mine and Earn\n\n…Loading…\n\nTo Proceed Please Click “Done” after Following our socials",
        reply_markup=reply_markup
    )

    # "DONE" button
    done_button = [[KeyboardButton("DONE", request_contact=False)]]
    reply_markup_done = ReplyKeyboardMarkup(done_button, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Click 'DONE' when you have followed our socials.", reply_markup=reply_markup_done)

    return ASK_USERNAME

async def ask_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Submit your X username (Example: @XXX)")
    return ASK_USERNAME + 1

async def save_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    x_username = update.message.text
    telegram_username = update.message.from_user.username

    # Thank You message
    await update.message.reply_text("Thank You")

    # Welcome message with image
    with open('coin_score.jpg', 'rb') as photo:  # Changed to .jpg
        await context.bot.send_photo(
            chat_id=update.message.chat_id,
            photo=photo,
            caption=f"Welcome to Chypto! [@{telegram_username}]\n\nMining Made Easy\n\nWe’re thrilled to have you join our community. Chypto is a thrilling game where you can experience the excitement of mining coins and convert to digital currency, and earn rewards.\n\nHere’s how to get started:\n\nStart Mining: Tap to mine resources and gather as much coins as possible.\nUpgrade Your Equipment: Use your resources to enhance your mining rigs for better efficiency.\nJoin Competitions: Participate in regular events to earn extra\nStay updated on our socials to get a chance to win quick $$$\nEarn and Withdraw: Convert your Coins into real Money and enjoy the fruits of your mining efforts.\nEnsure you Stay updated with our latest tips, tutorials, and event announcements"
        )

    # Buttons for Telegram channel and Web App
    buttons = [
        [InlineKeyboardButton("Follow our Channel", url="https://t.me/chyptochannel")],
        [InlineKeyboardButton("Play Chypto Game", web_app=WebAppInfo(url="https://chimajax.github.io/Chypto/index.html"))]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("Click the buttons below to stay updated and play the game.", reply_markup=reply_markup)

    # Save user data for future reference
    context.user_data['x_username'] = x_username
    context.user_data['telegram_username'] = telegram_username

    # Notify the referrer (assuming we have referrer info)
    referrer = context.user_data.get('referrer')
    if referrer:
        await context.bot.send_message(
            chat_id=referrer,
            text=f"Your referral @{telegram_username} has started playing Chypto!"
        )

    return ConversationHandler.END

async def remind_user(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    await context.bot.send_message(
        chat_id=job.context,
        text="Come Back and Earn & Check our socials for updates",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Follow our Channel", url="https://t.me/chyptochannel")],
            [InlineKeyboardButton("Play", web_app=WebAppInfo(url="https://chimajax.github.io/Chypto/index.html"))]
        ])
    )

async def set_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    # Schedule a reminder in 24 hours
    context.job_queue.run_once(remind_user, 86400, context=chat_id)

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ASK_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_username)],
            ASK_USERNAME + 1: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_username)],
        },
        fallbacks=[]
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('done', set_reminder))
    application.add_handler(MessageHandler(filters.COMMAND, set_reminder))

    application.run_polling()

if __name__ == '__main__':
    main()

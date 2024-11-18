import sqlalchemy as sa
from telegram.ext import ContextTypes

from bot_common.database import models
from bot_common.processors import broker, db


async def start(update, _: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_message = (
        "Welcome to the *Discount Alert Bot*\\! 🎉\n\n"
        "I'll help you track price drops on products you're interested in\\.\n"
        "Add a product link and specify the discount percentage\\, and I'll notify you when the price drops by that amount or more\\.\n\n"
        "📌 *How to use me:*\n"
        "1️⃣ *Add a product to your watch list:*\n"
        "`/add <link> <percentage>`\n"
        "Example\\: `/add https://www.example.com/product 15`\n\n"
        "2️⃣ *View your watch list:*\n"
        "`/list`\n\n"
        "3️⃣ *Remove a product from your list:*\n"
        "`/remove <product ID>`\n"
        "Example\\: `/remove 1`\n\n"
        "4️⃣ *Update the discount percentage for a product\\:*\n"
        "`/update <product ID> <new percentage>`\n"
        "Example\\: `/update 1 20`\n\n"
        "I'll check the prices daily at 12:00 PM and notify you of any discounts\\. 🛍️💰\n\n"
        "Happy savings\\! If you need help\\, just type `/help`\\."
    )
    await update.message.reply_markdown_v2(welcome_message)


async def add(update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        args = context.args
        if len(args) < 2:
            raise ValueError("Not enough arguments")
        url = args[0]
        discount = float(args[1])
        user_id = update.effective_user.id

        # Send task to Celery
        broker.send(
            task_data={"user_id": user_id, "link": url, "notification_threshold": discount},
            queue="live",
            task_name="add_product",
        )

        await update.message.reply_text("Product added to your watch list 🎉")
    except (IndexError, ValueError):
        await update.message.reply_markdown_v2(
            "Invalid command format\\. Use\\:\n"
            "`/add <link> <percentage>`\n"
            "Example\\: `/add https://www.example.com/product 15`"
        )


async def list_products(update, _: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id

    products = db.execute(sa.select(models.Product).where(models.Product.user_id == user_id)).all()

    if products:
        response = "📝 *Your Watch List:*\n"
        for idx, product in enumerate(products, 1):
            response += f"{idx}. {product['url']} - {product['discount']}%\n"
        await update.message.reply_markdown_v2(response)
    else:
        await update.message.reply_text("Your watch list is empty")


async def remove(update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) < 1:
            raise ValueError("Not enough arguments")
        product_id = int(args[0])
        user_id = update.effective_user.id

        # Send task to remove product
        broker.send(task_data={"user_id": user_id, "product_id": product_id}, queue="live", task_name="remove_product")

        await update.message.reply_text("Product removed from your list")
    except (IndexError, ValueError):
        await update.message.reply_markdown_v2(
            "Invalid command format\\. Use\\:\n`/remove <product ID>`\nExample\\: `/remove 2`"
        )


async def update_product(update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) < 2:
            raise ValueError("Not enough arguments")
        product_id = int(args[0])
        new_discount = float(args[1])
        user_id = update.effective_user.id

        # Send task to update discount threshold
        broker.send(
            task_data={"user_id": user_id, "product_id": product_id, "notification_threshold": new_discount},
            queue="live",
            task_name="update_product",
        )

        await update.message.reply_text("Discount percentage updated")
    except (IndexError, ValueError):
        await update.message.reply_markdown_v2(
            "Invalid command format\\. Use\\:\n"
            "`/update <product ID> <new discount percentage>`\n"
            "Example\\: `/update 2 25`"
        )

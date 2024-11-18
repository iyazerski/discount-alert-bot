import sqlalchemy as sa
from pydantic import ValidationError
from telegram.ext import ContextTypes

from bot_common.database import models
from bot_common.processors import broker, db
from bot_interface import schemas, utils


async def start(update, _: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_message = (
        "Welcome to the *Discount Alert Bot*\\! 🎉\n\n"
        "I'll help you track price drops on products you're interested in\\.\n"
        "Add a product link and specify the discount percentage, and I'll notify you when the price drops by that amount or more\\.\n\n"
        "📌 *How to use me:*\n"
        "1️⃣ *Add a product to your watch list:*\n"
        "`/add <product link> <discount percentage>`\n"
        "Example: `/add https://www.example.com/product 15`\n\n"
        "2️⃣ *View your watch list:*\n"
        "`/list`\n\n"
        "3️⃣ *Remove a product from your list:*\n"
        "`/remove <product link>`\n"
        "Example: `/remove https://www.example.com/product`\n\n"
        "4️⃣ *Update the discount percentage for a product:*\n"
        "`/update <product link> <new discount percentage>`\n"
        "Example: `/update https://www.example.com/product 20`\n\n"
        "I'll check the prices daily at 12:00 PM and notify you of any discounts\\. 🛍️💰\n\n"
        "Happy savings\\! If you need help, just type `/help`\\."
    )
    await update.message.reply_markdown_v2(welcome_message)


async def add(update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Parse and validate arguments
        if not context.args or len(context.args) < 2:
            raise ValueError("Not enough arguments")
        model = schemas.AddProductModel(product_link=context.args[0], discount=context.args[1])
        user_id = update.effective_user.id

        # Send task to Celery
        broker.send(
            task_data={
                "user_telegram_id": user_id,
                "product_link": str(model.product_link),
                "notification_threshold": model.discount,
            },
            queue="live",
            task_name="add_product",
        )

        await update.message.reply_text("Product added to your watch list 🎉")
    except (ValidationError, IndexError, ValueError) as e:
        error_message = utils.extract_error_message(e)
        await update.message.reply_markdown_v2(
            f"*Invalid command format:*\n{error_message}\n"
            "_Use:_ `/add <product link> <discount percentage>`\n"
            "_Example:_ `/add https://www.example.com/product 15`"
        )


async def list_products(update, _: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id

    with db.connect():
        products: list[models.Product] = db.execute(
            sa.select(models.Product).join(models.Product.user).where(models.User.telegram_id == user_id)
        ).all()

        if products:
            response = "<b>📝 Your Watch List:</b>\n\n"
            for idx, product in enumerate(products, 1):
                response += (
                    f'{idx}. <a href="{product.link}">{product.link}</a>\n'
                    f"initial price - <b>{product.initial_price}</b>, "
                    f"waiting for <b>{product.notification_threshold}%</b> discount\n"
                )
            await update.message.reply_html(response)
        else:
            await update.message.reply_text("Your watch list is empty")


async def remove(update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Parse and validate arguments
        if not context.args:
            raise ValueError("Not enough arguments")
        model = schemas.RemoveProductModel(product_link=context.args[0])
        user_id = update.effective_user.id

        # Send task to remove product
        broker.send(
            task_data={"user_telegram_id": user_id, "product_link": str(model.product_link)},
            queue="live",
            task_name="remove_product",
        )

        await update.message.reply_text("Product removed from your list")
    except (ValidationError, ValueError) as e:
        error_message = utils.extract_error_message(e)
        await update.message.reply_markdown_v2(
            f"*Invalid command format:*\n{error_message}\n"
            "_Use:_ `/remove <product link>`\n_Example:_ `/remove https://www.example.com/product`"
        )


async def update_product(update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Parse and validate arguments
        if not context.args or len(context.args) < 2:
            raise ValueError("Not enough arguments")
        model = schemas.AddProductModel(product_link=context.args[0], discount=context.args[1])
        user_id = update.effective_user.id

        # Send task to update discount threshold
        broker.send(
            task_data={
                "user_telegram_id": user_id,
                "product_link": str(model.product_link),
                "notification_threshold": model.discount,
            },
            queue="live",
            task_name="update_product",
        )

        await update.message.reply_text("Discount percentage updated")
    except (ValidationError, ValueError) as e:
        error_message = utils.extract_error_message(e)
        await update.message.reply_markdown_v2(
            f"*Invalid command format:*\n{error_message}\n"
            "_Use:_ `/update <product link> <new discount percentage>`\n"
            "_Example:_ `/update https://www.example.com/product 25`"
        )

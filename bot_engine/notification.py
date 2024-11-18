from telegram import Bot

from bot_common.processors import settings


async def send_notification(user_telegram_id: str, product_link: str, current_price: str):
    async with Bot(token=settings.TELEGRAM_BOT_TOKEN.get_secret_value()) as bot:
        await bot.send_message(
            chat_id=user_telegram_id,
            text=(
                f"*Good news\\!* 🎉\n\n"
                f"The price for [{product_link}]({product_link}) has dropped to *{current_price}*\\. 🛍️💰\n\n"
                "Don't miss out on this deal\\!"
            ),
            parse_mode="MarkdownV2",
        )

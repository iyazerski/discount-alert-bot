# discount-alert-bot

`discount-alert-bot` is a Telegram chatbot that notifies users about discounts on products from their wish lists. Users can add product links and set a desired percentage price drop for notifications. The bot periodically checks the prices and sends alerts when discounts meet the user’s criteria.

## Features

- Add Products: Users can add product links to their wish list directly through the chatbot.
- Set Price Drop Alerts: Specify the percentage decrease in price at which you want to be notified.
- Automatic Price Checking: The bot checks prices daily at 12:00 PM.
- Notifications: Receive Telegram messages when your desired products go on sale.
- Manage Wish List: Remove products or adjust alert thresholds at any time.

## Architecture Overview

The project consists of two main services:
1. `bot-interface`: Handles user interactions via Telegram and communicates with `bot-engine` through API calls and message queues.
2. `bot-engine`: Processes tasks such as parsing product pages and checking for price drops. It interacts with the PostgreSQL database and uses Celery for task scheduling.

## Installation

### Prerequisites

- Docker and Docker Compose installed on your machine
- Telegram account to interact with the bot
- API keys for OpenAI and Telegram Bot API

### Clone the Repository

```shell
git clone https://github.com/iyazerski/discount-alert-bot.git
cd discount-alert-bot
```

### Configure Environment Variables

Create a `.env` file in both the `bot-interface` and `bot-engine` directories with the following variables:

**bot_interface/.env**
```text
# api keys
BOT_INTERFACE_API_KEY=your_bot_interface_api_key
TELEGRAM_API_KEY=your_telegram_api_key

# broker
BROKER_HOST=localhost
BROKER_PORT=5672
BROKER_USERNAME=user
BROKER_PASSWORD=password
```

**bot_engine/.env**
```text
# api keys
BOT_INTERFACE_API_KEY=your_bot_interface_api_key
OPENAI_API_KEY=your_openai_api_key

# db
DB_HOST=localhost
DB_PORT=27017
DB_USERNAME=user
DB_PASSWORD=password

# broker
BROKER_HOST=localhost
BROKER_PORT=5672
BROKER_USERNAME=user
BROKER_PASSWORD=password
```

#### Build and Run with Docker Compose

```shell
docker compose up --build
```

This command will set up the following containers:
- discount-alert-bot-interface
- discount-alert-bot-engine
- discount-alert-bot-rabbitmq
- discount-alert-bot-postgres
- discount-alert-bot-celery-worker

## Usage

1. Start the Bot: Ensure the Docker containers are running.
2. Interact via Telegram: Find your bot on Telegram using the bot username you set up with BotFather.
3. Commands:

   - /start: Get a welcome message and help information.
   - /add {product_link} {price_drop_percentage}: Add a new product to your wish list.
   - /list: View all products in your wish list.
   - /remove {product_link}: Remove a product from your wish list.
   - /update {product_link} {new_price_drop_percentage}: Update the alert threshold for a product.

## License

This project is licensed under the MIT License.

## Contact

For questions or support, please open an issue in the GitHub repository.

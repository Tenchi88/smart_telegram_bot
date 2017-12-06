# smart_telegram_bot
Smart bot for telegram with easily configurable logic.

You have to place valid Telegram bot token to 'json_configs/telegram.json' in defaulf configuration.

This file has format:
{
  "token": "YOUR_TOKEN"
}

Also you need to specify 'SECRET_KEY' value for Django in 'web/django_private_settings.py'

* 'classifiers/' - base class and classifiers examples for nodes
* 'json_configs/' - .json with logical configuration, etc.
* 'logger/' - interface for messages logging into db
* 'nodes/' - nodes and nodes tree definition
* 'nodes_app/' - Django application with web interface for logical configuration
* 'train_sets/' - train sets for classifiers
* 'web' - Django project


Usage

Specify telegram token as described before, than run: 'python smart_telegram_bot.py'

Language: Python 3
OS: macOS/Linux(wasn't tested on Windows)
import logging

BACKEND = 'Telegram'

BOT_DATA_DIR = r'./data'
BOT_EXTRA_PLUGIN_DIR = r'./plugins'

BOT_LOG_FILE = r'./errbot.log'
BOT_LOG_LEVEL = logging.DEBUG

# Bot Administrators ID
BOT_ADMINS = (123456789, )

BOT_IDENTITY = {
    'token': '1290489125:wefjnwgjenrjgnehnertgiengeonjg',
}

# Telegram specific settings as mentioned in the docs
BOT_PREFIX = '/'
CHATROOM_PRESENCE = ()

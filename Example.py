import logging
from chathandler import TTChatBotLoggingHandler

if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s",
                        level=logging.INFO,
                        datefmt="%m/%d/%Y %I:%M:%S %p")
    handler = TTChatBotLoggingHandler(config='config.json')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger = logging.getLogger('Bot_example')
    logger.addHandler(handler)
    logger.info('test')
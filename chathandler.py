import os
import logging
import requests
import json
from logging import StreamHandler
import BotLoggingException


class TTChatBotLoggingHandler(StreamHandler):
    """
    https://dev.tamtam.chat/
    """

    def __init__(self, config):
        StreamHandler.__init__(self)
        with open(config, 'r', encoding='utf-8') as c:
            self.config = json.load(c)
        self.token = self.config['access_token']
        self.chat_id = self.config['chat_id']
        # to use this bot you have to obtain chat_id, where bot will send log messages, the appropriate method is below
        # this is optional for your environment, enter <you proxy here> if you have a proxy
        self.url = 'https://botapi.tamtam.chat/'

    def emit(self, record):
        msg = self.format(record)
        self.send_message(msg, self.chat_id)

    def get_chat_id(self):
        """
        Before using this bot you must obtain chat_id, where bot will send log messages
        To do this run this method and write to bot something, and then method immediately return chat_id
        chat_id changes when you create group chat
        :return: integer chat_id
        """
        while True:
            response = self.get_updates()
            try:
                chat_id = response['updates'][0]['message']['recipient']['chat_id']
                self.send_message("Your chat id is {}".format(chat_id), chat_id)
                return chat_id
            except IndexError:
                continue

    def send_message(self, text, chat_id):
        """
        Send message to specific chat_id by post request
        :param text: text of message
        :param chat_id: integer, chat id of user
        :return:
        """
        url = ''.join([self.url, 'messages?access_token=', self.token, '&chat_id={}'.format(chat_id)])
        params = {"text": text}
        response = requests.post(url, data=json.dumps(params))
        if response.status_code != 200:
            raise BotLoggingException("Error sending message: {}".format(response.status_code))

    def get_updates(self):
        """
        This method is used to get updates from bot via get request. It is based on long polling.
        https://dev.tamtam.chat/#operation/getUpdates
        """
        params = {
            "timeout": 90,
            "limit": 1000,
            "marker": None,
            "types": None,
            "access_token": self.token
        }
        response = requests.get(self.url + 'updates', params)
        return response.json()


if __name__ == '__main__':
    handler = TTChatBotLoggingHandler(config='config.json')
    print(handler.get_chat_id())
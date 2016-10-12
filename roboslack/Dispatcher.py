import asyncio
import re
import logging
from slacksocket.models import SlackEvent
from slacksocket import SlackSocket
from roboslack.Exceptions import ClientCannotBeEmptyException
from roboslack.MessageTypes import message_types

logging.basicConfig(level=logging.INFO)


class Dispatcher(object):
    def __init__(self, client, log=None):
        """

        :param client:
        :type client: SlackSocket
        :param log:
        :type log: logging.Logger
        """
        if not log:
            log = logging.getLogger('roboslack:dispatcher')

        if not client:
            raise ClientCannotBeEmptyException

        self.__client = client
        self.log = log
        self.__user_list = []
        for user in self.__client.loaded_users:
            self.__user_list.append(user.get('name'))

    def say(self, message, event):
        """
        Reply to a user message

        :param message:
        :type message: str
        :param event:
        :type event: SlackEvent
        :return:
        :rtype:
        """
        if self.__client.user in event.mentions and event.event.get('channel') not in self.__user_list:
            msg = self.__client.send_msg(
                message,
                channel_name=event.event.get('channel'),
                confirm=False
            )
        else:
            msg = self.__client.send_msg(
                message,
                channel_id=self.__client.get_im_channel(
                    event.event.get('channel')
                ).get('id'),
                confirm=False
            )

        if 'msg' in locals():
            self.log.info(" Message sent {}".format(msg.json))

    @asyncio.coroutine
    def handle(self, event, task_id):
        """

        :param event:
        :type event: SlackEvent
        :param task_id:
        :type task_id: int
        :return:
        :rtype:
        """

        text = self.__remove_mentions(event.event.get('text')).strip()

        if self.__client.user in event.mentions:
            self.__handle_mention(event, text, task_id)
        elif event.event.get('channel') in self.__user_list:
            self.__handle_direct_message(event, text, task_id)

        yield from asyncio.sleep(2.5)

    def __handle_mention(self, event, text, task_id):
        self.log.info("{}: Got mentioned in channel {} by {}".format(
            task_id,
            event.event.get('channel'),
            event.event.get('user')
        ))
        for pattern, func in message_types['mention'].items():
            pattern = re.compile(pattern, re.IGNORECASE)
            if pattern.findall(text):
                self.log.info("{}: Calling function {}".format(task_id, func.__name__))
                return func(event, *pattern.findall(text))

    def __handle_direct_message(self, event, text, task_id):
        self.log.info("{}: Got a private message by {}".format(
            task_id,
            event.event.get('user')
        ))
        for pattern, func in message_types['direct_message'].items():
            pattern = re.compile(pattern, re.IGNORECASE)
            if pattern.findall(text):
                self.log.info("{}: Calling function {}".format(task_id, func.__name__))
                return func(event, *pattern.findall(text))

    @staticmethod
    def __remove_mentions(text):
        return re.sub('<[^>]+>', '', text)

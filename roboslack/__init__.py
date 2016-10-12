import asyncio
from multiprocessing import cpu_count
from os import getenv
from slacksocket import SlackSocket
import logging
from roboslack.Dispatcher import Dispatcher
from roboslack.Exceptions import SlackAPIKeyNotSpecified, InvalidMessageType
from roboslack.MessageTypes import message_types


class RoboSlack(object):
    def __init__(self, api_key=None, filters=None):
        """

        :param api_key:
        :type api_key:
        """
        if filters is None:
            filters = ["message"]

        if not api_key:
            if getenv('SLACK_API_KEY'):
                api_key = getenv('SLACK_API_KEY')
            else:
                raise SlackAPIKeyNotSpecified

        self.__slack = SlackSocket(
            api_key,
            event_filters=filters
        )
        self.log = logging.getLogger('roboslack')
        logging.basicConfig(level=logging.INFO)
        self.__dispatcher = Dispatcher(self)

    def client(self):
        """

        :return:
        :rtype: SlackSocket
        """
        return self.__slack

    def name(self):
        """

        :return:
        :rtype: str
        """
        return self.client().user

    @asyncio.coroutine
    def _start_rtm(self, task_id=0):
        """

        :return:
        :rtype:
        """
        for event in self.client().events():
            yield from self.__dispatcher.handle(event, task_id)

    def run(self):
        log = logging.getLogger('roboslack:executor')
        loop = asyncio.get_event_loop()
        tasks = []
        if cpu_count() <= 3:
            threads = 4
        else:
            threads = cpu_count()

        for i in range(0, threads):
            tasks.append(
                asyncio.ensure_future(
                    self._start_rtm(i)
                )
            )
        log.info("Starting {} threads for the dispatcher, press Ctrl+C to interrupt.".format(threads))

        loop.run_until_complete(
            asyncio.gather(
                *tasks
            )
        )

    @staticmethod
    def on(message_type, expression, func):
        """
        Subscribe the bot to a type of message

        :return:
        :rtype:
        """
        if message_type not in message_types:
            raise InvalidMessageType(message_type)

        message_types[message_type][expression] = func

    def say(self, message, event):
        """
        Reply to a user message

        :param message:
        :type message: str
        :param message:
        :type message: SlackEvent
        :return:
        :rtype:
        """
        self.__dispatcher.say(message, event)

    def reply(self, message, event):
        """
        Reply to a user message

        :param message:
        :type message: str
        :param message:
        :type message: SlackEvent
        :return:
        :rtype:
        """
        self.__dispatcher.say(message, event)
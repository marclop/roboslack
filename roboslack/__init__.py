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

        :param api_key: Slack API Key
        :type api_key: str
        :param filters:
        :type filters: list of str
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
        self.__dispatcher = Dispatcher(self.client())

    def client(self):
        """
        Get the SlackSocket client

        :return:
        :rtype: SlackSocket
        """
        return self.__slack

    def name(self):
        """
        Get the bot name

        :return:
        :rtype: str
        """
        return self.client().user

    @asyncio.coroutine
    def _start_rtm(self, task_id=0):
        """
        Consume events

        :return:
        :rtype:
        """
        for event in self.client().events():
            yield from self.__dispatcher.handle(event, task_id)

    def run(self):
        """
        Start processing slack messages by RoboSlack

        :return:
        :rtype:
        """
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

        self.log.info(
            "Starting {} threads for the dispatcher, press Ctrl+C to interrupt.".format(
                threads
            )
        )
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            asyncio.gather(
                *tasks
            )
        )

    @staticmethod
    def on(message_type, expression, func):
        """
        Subscribe the bot to a type of message

        Function signature is:
            def function(event, *args)

        :param message_type: Either `direct_message` or `mention`
        :type message_type: string
        :param expression: Regex or word to which react
        :type expression: str
        :param func: Definition of the function to pass
        :type func:
        :return:
        :rtype: None
        """
        if message_type not in message_types:
            raise InvalidMessageType(message_type)

        message_types[message_type][expression] = func

    def on_mention(self, expression, func):
        """
        Subscribe the bot to mentions matching the expression

        Function signature is:
            def function(event, *args)

        :param expression: Regex or word to which react
        :type expression: str
        :param func: Definition of the function to pass
        :type func:
        :return:
        :rtype: None
        """
        self.on('mention', expression, func)

    def on_direct_message(self, expression, func):
        """
        Subscribe the bot to direct messages matching the expression

        Function signature is:
            def function(event, *args)

        :param expression: Regex or word to which react
        :type expression: str
        :param func: Definition of the function to pass
        :type func:
        :return:
        :rtype: None
        """
        self.on('direct_message', expression, func)

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

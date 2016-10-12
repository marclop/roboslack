# RoboSlack
[![PyPI version](https://badge.fury.io/py/roboslack.svg)](https://badge.fury.io/py/roboslack)

RoboSlack is a [Slack](https://slack.com/) bot python framework that allows you to create simple enough bots

# Features

* Regexp matching
* RTM integration
* Thread support

## Missing
* Conversational
* Tests

# Installation
*NOTE: RoboSlack requires python version 3.4+*

```bash
pip install roboslack
```

# Configuration parameters
There's just one configuration parameter, `SLACK_API_KEY` environment variable, setting that to the appropriate
Slack token key will allow you to connect to the RTM API for Slack, for more information on that, visit Slack's
[documentation](https://api.slack.com/bot-users)

# Usage

To create a simple bot, you could use this snippet, which will allow you to greet the bot.
```python
from roboslack import RoboSlack

bot = RoboSlack()


def reply_to_hi(event, *args):
    bot.say("hi dude", event)


bot.on(
    'mention',
    '^hi',
    reply_to_hi
)
bot.on(
    'direct_message',
    '^hi',
    reply_to_hi
)

bot.run()
```

## Message types
To listen to different types of messages you can choose from `mention` and `direct_message`.


# Example application

You can check out an example of how to use *roboslack* framework in the [examples](examples/) folder.

# Contributing

To develop the bot is as easy as having [Docker](https://docs.docker.com/#/components) and [docker-compose](https://docs.docker.com/compose/install/) installed, then typing `make`
will start the development environment for the bot. (Requires `SLACK_API_KEY` environment variable) set in your current terminal.

# License
MIT License

Copyright (c) 2016 Marc Lopez Rubio

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
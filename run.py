from roboslack import RoboSlack


def reply_to_hi(event, *args):
    bot.say("hi dude", event)


def say_something(event, *args):
    bot.say("{}".format(*args), event)


if __name__ == "__main__":
    bot = RoboSlack()

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
    bot.on(
        'direct_message',
        'say (.*)',
        say_something
    )

    bot.run()

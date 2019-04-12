[![Build Status](https://travis-ci.org/haandol/honey.svg?branch=master)](https://travis-ci.org/haandol/honey)

# Honey

A neat [Slack](slack.com) bot for Pythonistas

## Dependencies

Python3.5+ (for async/await)

[redis](https://github.com/andymccurdy/redis-py), [slackclient](https://github.com/slackhq/python-slackclient).

```bash
$pip install -r requirements.txt
```

## Usage

Like Django, you can config your bot by editing `settings.py`

set `SLACK_TOKEN` variable in settings.py.
if `REDIS_URL` or `REDIS_PORT` is not setted, all Redis relevant features, like redis_brain, will be disabled.

### Congiure your bot

1. Add your bot for your slack account at [Custom Integration Page](https://my.slack.com/services/new/bot)
2. Copy API Token to clipboard.
2. Open `settings.py`
3. Set `SLACK_TOKEN`. You can set `REDIS_URL` if it's available.
4. Run `$python robot.py`
5. Invite your bot to the channel `/invite @YOUR_BOT_NAME`

### Play with it on the Slack

Type command with Command Prefix (default is `!` ) on the channel where the bot is on.

Honey is going to respond to your command kindly.

```
YOU: !help

Honey: Hello world!!
```

## Apps

We call each function that you plugged-in to the Honey, the app.

Built-in and example apps are in the `apps` directory.

### App and Command

Below is basic form of app.
It just says `Hello world!!` to the channel that user typed the command, `!hi`.

```python
@on_command(['hi', 'hello', '하이', 'ㅎㅇ'])
def hello_world(robot, channel, user, tokens):
    '''
        Simple app just says `Hello word!!`

        @params {object} robot - Honey bot instance
        @params {str} channel - channel name where invoked this app
        @params {str} user - user id who invoked this app
        @params {list} tokens - user input tokens
        @returns {str, str} - channel name, message
    '''
    return channel, 'Hello world!!'
```

And Honey supports multiple commands for each function.

The above app can be invoked the command with Command Prefix (default is `!`) on the channel.
It would be `!hello`, `!hi`, `!하이` or '!ㅎㅇ'


### Tokenizer

Honey automatically split your message into tokens by whitespaces.

Let's assume that you typed `!memo remember this` with blow app.

```python
@on_command(['memo'])
def remember(robot, channel, user, tokens):
    assert 2 == len(tokens)
    assert 'remember' == tokens[0]
    assert 'this' == tokens[1]
    return channel, tokens[1]
```

You may want tokens containing whitespaces.
In that case, wrap your token with double quote(") like

```bash
!memo remember "kill -9 $(ps aux | grep gunicorn | grep -v 'grep' | awk '{print $2 }')"
```

### Redis Brain

Honey supports semi-permanent storage using Redis as well as Hubot.

Let's assume that you typed `!memo whats this` in your channel with below app.

after that, whenever you type `!memo whats` Honey will says `this` to the channel.

### Register your app

1. Add your app and put it into `apps` folder
2. open `settings.py` and add your app name(like 'hello_world') to `APPS`
3. restart your bot

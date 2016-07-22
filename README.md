[![Build Status](https://travis-ci.org/haandol/honey.svg?branch=master)](https://travis-ci.org/haandol/honey)

# Honey

A neat [Slack](slack.com) bot for Pythonistas

## Dependencies

requires [gevent](https://github.com/gevent/gevent), [redis](https://github.com/andymccurdy/redis-py), [slackclient](https://github.com/slackhq/python-slackclient).

```bash
$pip install -r requirements.txt
```

## Usage

Like Django, you can config your bot by editing `settings.py`

set your `SLACK_TOKEN` and `REDIS_URL` in settings.py.
if REDIS_URL does not set, all REDIS relevant features will be ignored.

### Congiure your bot

1. Add your bot for your slack account at [Custom Integration Page](https://buzzni.slack.com/apps/manage/custom-integrations)
2. open settings.py
3. set `SLACK_TOKEN`. You can set `REDIS_URL` if it's available.
4. run `$python robot.py`

### Play with it on the Slack

Type command with COMMAND_PREFIX (e.g. `!` ) on the channel where the bot is on.

Bot is going to respond to your commands if your bot is on the channel where you type the command.

```
!help
!hi
```

## Apps

Example apps are in the apps directory.

### Command

Honey supports multiple commands for a function

```python
@on_command(['하이', 'hi', 'hello'])
def hello_world(robot, channel, user, tokens):
    return 'Hello world!!'
```

then type your command with COMMAND_PREFIX (e.g. `!`) on the channel that including bot
like `!hi` or `!hello` or `!하이`


### Tokenizer

Honey automatically split your message into tokens by whitespaces

Let's assume that you typed `!memo recall this` in your channel

```python
@on_command(['memo'])
def recall(robot, channel, user, tokens):
    assert 2 == len(tokens)
    assert 'recall' == tokens[0]
    assert 'this' == tokens[1]
```

Sometimes you want tokens containing whitespaces,
in that case, wrap your token with double quote(") like

```bash
!memo kill "kill -9 $(ps aux | grep gunicorn | grep -v 'grep' | awk '{print $2 }')"
```

### Redis Brain

Honey supports semi-permanent storage using redis as well as Hubot.

Let's assume that you typed `!memo recall this` in your channel

```python
@on_command(['ㄱㅇ', '기억', 'memo'])
def redis_brain(robot, channel, user, tokens):
    assert 2 == len(tokens)
    key = tokens[0]
    value = tokens[1]
    robot.brain.set(key, value)

    return robot.brain.get(key)
```

then, Honey would say `this` to the channel

### Register your app

1. Add your app and put it into `apps` folder
2. open `settings.py` and add your app name(like 'hello_word') to `APPS`
3. restart your bot

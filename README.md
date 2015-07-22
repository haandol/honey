# Hongmoa

A Slack(slack.com) for Pythonistas

## Dependencies

Hongmoa requires [gevent](https://github.com/gevent/gevent), [redis](https://github.com/andymccurdy/redis-py), [slackclient](https://github.com/slackhq/python-slackclient).

## Configuration

Like Django, you can config your bot by editing settings.py

## Installation

```bash

$pip install -r requirements.txt

$python robot.py

```

## Apps

Examples are included in the apps directory.


### Command

Hongmoa supports multiple commands for a function

```python
@on_command(['하이', 'hi', 'hello'])
def hello_world(robot, channel, tokens):
    return 'Hello world!!'
```

then type your command with prefix `!` in the channel that including bot
like `!hi` or `!hello` or `!하이`


### Tokenizer

Hongmoa automatically split your message into tokens by whitespaces

Let's assume that you typed `!memo recall this` in your channel

```python
@on_command(['memo'])
def recall(robot, channel, tokens):
    assert 2 == len(tokens)
    assert 'recall' == tokens[0]
    assert 'this' == tokens[1]
```

Sometimes you want to tokens containing whitespaces,
in that case, wrap your token with double quote(") like

```bash
!memo kill "kill -9 $(ps aux | grep gunicorn | grep -v 'grep' | awk '{print $2 }')"
```

### Redis Brain

Hongmoa supports semi-permanent storage using redis as well as Hubot.

Let's assume that you typed `!memo recall this` in your channel

```python
@on_command(['ㄱㅇ', '기억', 'memo'])
def redis_brain(robot, channel, tokens):
    assert 2 == len(tokens)
    key = tokens[0]
    value = tokens[1]
    robot.brain.set(key, value)

    return robot.brain.get(key)
```

then, Hongmoa would say `this` to the channel

reddit-new-post-notify
======================

Very small python3 script for doing a task for every new post on a specific sub

How to use
----------
Run it with docker.  Sample docker-compose example below:
```
reddit-new-post-notify-pushover:
    image: python:slim
    container_name: reddit-new-post-notify-pushover
    environment:
        - PUSHOVER_TOKEN=
        - PUSHOVER_USER_KEY=
        - UPDATE_INTERVAL=60
        - SUBREDDIT=aww
    volumes:
        - $HOME/notifier.py:/usr/src/script.py

    command: python -u /usr/src/script.py
    restart: always
```

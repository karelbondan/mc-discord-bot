# Minecraft x Discord Bot

A simple discord bot that listens the log of a Minecraft Java server. This bot currently only supports one minecraft server and one discord server with one text channel. There is no plan to expand it to handle multiple server at once. If you want to use this bot, you should run this bot on your own.

All of the bot configurations can be adjusted in `config.yml`, with the sensitive data being mandatory to be put inside a `.env` file.

## Tech stacks

- discord.py
- pygtail
- minecraft server (spigot in this case)
- mojang moment

## Features

- Sends world events to a designated channel on a discord server. Events include:
  - Player joining and leaving
  - Player messages
  - Player deaths
  - Player accomplishing an achievement
- Sends a message sent on a designated channel on a discord server to the minecraft server.
- Lets users know when the server is offline

## Known bug(s)

None. I'm the best.

## Upcoming feature(s)

- Bedrock player skins would be visible on the embed (currently they default to Steve).
- Start, restart server through bot command (need to implement check before restarting. Wouldn't want to restart if there are still players on the server).

## `.env` fields

```py
# minecraft 
MC_HOST="0.0.0.0"
MC_PORT=55000

# rcon
RCON_PASS="password"
RCON_PORT=25575

# bot token
TOKEN="token"
```

> (c) 2026 Karel Bondan

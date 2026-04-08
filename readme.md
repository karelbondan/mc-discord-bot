# Minecraft x Discord Bot

A simple discord bot that listens the log of a Minecraft Java server. This bot
currently only supports one server and there is no plan to expand it to hande
multiple server at once. If you want to use this bot, you should run this bot on
your own.

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
RCON_PASS="password"
TAB_AMT=5
TOKEN="token"
HEAD_URL="https://minotar.net/helm/{}/32.png"
BODY_URL="https://minotar.net/armor/body/{}/150.png"
EMOJI_REPLY="<:tree:1297239384864718920>"
EMOJI_END="<:tree_end:1297239401751122001>"
EMOJI_JOIN="<:join:1297239340082270288>"
EMOJI_LEAVE="<:leave:1297239361858830396>"
WEBHOOK_URL_OLD="https://discord.com/api/webhooks/1189197056020054057/gpljFuylsUMh2wknvACZL4NAFpQPCaqoW3PaYE4WbwL11uM4215afOAWplCXAsu1Qlq6{}?wait=true"
WEBHOOK_URL="https://discord.com/api/webhooks/1294613253615517758/x--8uJ-I2WGNBdXSo5MKKu7WJ8z_Z8iXXElGfYWxHQ3AJWBheSoXNWjouhMjjLWa6B9G{}?wait=true"
NOT_DEATHS=["Thread","Saving","Stopping","server operator","Using","Debug logging","Generating","Loaded","Hooked","TreeCuter","Did not hook","Linked","Finished","Showing new","Loading","Preparing","Reset","The difficulty","joined","left"]
```

> (c) 2026 Karel Bondan

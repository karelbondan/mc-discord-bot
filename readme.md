# Minecraft x Discord Bot

A simple discord bot that listens the log of a Minecraft Java server. This bot
currently only supports one server and there is no plan to expand it to hande 
multiple server at once. If you want to use this bot, you should run this bot on
your own. 

## Tech stacks 

- discord.py 
- pygtail (to be implemented) 
- minecraft server (spigot in this case)
- mojang moment 

## Features 

- Sends world events to a designated channel on a discord server. Events include:
	- Player joining and leaving
	- Player messages
	- Player deaths
	- Player accomplishing an achievement
- Sends a message sent on a designated channel on a discord server to the minecraft server.

## Known bug(s)
Since the current reading algorithm is not optimized yet, sometimes logs get skipped 
since the minecraft server can dump the logs really fast. Going to try implementing
a new algorithm using pygtail to address this issue. 

> (c) 2025 Karel Bondan

# Dinos in Donut Dungeons

Simple PyGame with included multiplayer using PubNub platform

## Game objectives and controls

You are a Dinosaur in a Dungeon. You eat Donuts

Movement: `WSAD` Keys

Look aroung: Mouse

Fullscreen: `F` Key

Exit: `ESC` Key

## Install and run:

Clone this repo:

```
git clone https://github.com/seba-aln/DinosDonutDungeons.git && cd DinosDonutDungeons
```

Prepare Python's virtual environment:

```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

Setup your PubNub keys and a player name. You'll need keys that you can get [here](https://admin.pubnub.com/) for free!
All other players have to have the same keyset to play together!

```
./setup.sh
```

Run the game:

```
python main.py
```
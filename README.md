# Pack Mashup Maker

This is a tool to create a pack mashup from a list of packs.

## Installation

- Install [Python 3](https://www.python.org/downloads/)
- Install dependencies: `py -m pip install -r requirements.txt`
- Run the program (replace any text `<LIKE THIS>` with what would go there, the text should explain it): `py main.py --name=<NAME> --description=<DESCRIPTION> --input=<PATH TO FOLDER WITH INPUT PACKS>`

## Arguments

- `--name`: The name of the pack mashup, if missing, it will prompt you for it.
- `--description`: The description of the pack mashup, if missing, it will prompt you for it.
- `--input`: The path to the folder with the input packs, if missing, will default to `%appdata%\.minecraft\resourcepacks`. If `temp/` exists in the folder, it will use that instead.
- `--disable-preview-gen`: Will not generate preview images, this is useful if you already have the preview images generated and don't want to wait for them to be generated again.
- `--no-credits`: Will not generate a credits.txt file, I recommend you don't use this as some authors may not want their pack to be used in a mashup without credit.

## Supported block/item categories

- Clay
- Tools
- Shears
- Wool
- Bow
- Apple
- Armour items
- Buckets
- Endstone
- Wood
- Ladder
- Obsidian
- Sword
- Stick
- Armour model
- Arrow
- Projectiles
- Ender pearl
- GUI
- Fireballs
- TNT
- Sponge
- Chests
- Fishing rod
- Resource items
- Resource blocks
- Ore blocks
- Eyes of ender
- Ice
- Breaking Animation
- Bed
- Glass
  
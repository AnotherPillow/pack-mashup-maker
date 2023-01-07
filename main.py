import os,re,time,json, argparse, shutil
from PIL import Image
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file, jsonify
from remove_extra import remove_extra
from unzip import unzip

parser = argparse.ArgumentParser()
parser.add_argument('--disable-preview-gen', action='store_true', help='Disable generation of preview images')
parser.add_argument('--no-credits', action='store_true', help='Why, just why would you use this?')
parser.add_argument('--input', action='store', help='Path to the resourcepacks folder')
parser.add_argument('--name', action='store', help='Name of the output pack')
parser.add_argument('--description', action='store', help='Description of the output pack')

args = parser.parse_args()

options = {
    'wool': [
        'assets/minecraft/textures/blocks/wool_colored_yellow',
        'assets/minecraft/textures/blocks/wool_colored_white',
        'assets/minecraft/textures/blocks/wool_colored_red',
        'assets/minecraft/textures/blocks/wool_colored_purple',
        'assets/minecraft/textures/blocks/wool_colored_pink',
        'assets/minecraft/textures/blocks/wool_colored_orange',
        'assets/minecraft/textures/blocks/wool_colored_magenta',
        'assets/minecraft/textures/blocks/wool_colored_lime',
        'assets/minecraft/textures/blocks/wool_colored_silver',
        'assets/minecraft/textures/blocks/wool_colored_light_blue',
        'assets/minecraft/textures/blocks/wool_colored_green',
        'assets/minecraft/textures/blocks/wool_colored_gray',
        'assets/minecraft/textures/blocks/wool_colored_cyan',
        'assets/minecraft/textures/blocks/wool_colored_brown',
        'assets/minecraft/textures/blocks/wool_colored_blue',
        'assets/minecraft/textures/blocks/wool_colored_black'
    ],
    'clay': [
        'assets/minecraft/textures/blocks/hardened_clay_stained_yellow',
        'assets/minecraft/textures/blocks/hardened_clay_stained_white',
        'assets/minecraft/textures/blocks/hardened_clay_stained_red',
        'assets/minecraft/textures/blocks/hardened_clay_stained_purple',
        'assets/minecraft/textures/blocks/hardened_clay_stained_pink',
        'assets/minecraft/textures/blocks/hardened_clay_stained_orange',
        'assets/minecraft/textures/blocks/hardened_clay_stained_magenta',
        'assets/minecraft/textures/blocks/hardened_clay_stained_lime',
        'assets/minecraft/textures/blocks/hardened_clay_stained_silver',
        'assets/minecraft/textures/blocks/hardened_clay_stained_light_blue',
        'assets/minecraft/textures/blocks/hardened_clay_stained_green',
        'assets/minecraft/textures/blocks/hardened_clay_stained_gray',
        'assets/minecraft/textures/blocks/hardened_clay_stained_cyan',
        'assets/minecraft/textures/blocks/hardened_clay_stained_brown',
        'assets/minecraft/textures/blocks/hardened_clay_stained_blue',
        'assets/minecraft/textures/blocks/hardened_clay_stained_black'
    ],
    'bow': [
        'assets/minecraft/textures/items/bow_standby',
        'assets/minecraft/textures/items/bow_pulling_0',
        'assets/minecraft/textures/items/bow_pulling_1',
        'assets/minecraft/textures/items/bow_pulling_2'
    ],
    'apple': [
        'assets/minecraft/textures/items/apple_golden',
        'assets/minecraft/textures/items/apple'
    ],
    'armour-items': [
        'assets/minecraft/textures/items/leather_helmet',
        'assets/minecraft/textures/items/leather_chestplate',
        'assets/minecraft/textures/items/leather_leggings',
        'assets/minecraft/textures/items/leather_boots',
        'assets/minecraft/textures/items/iron_helmet',
        'assets/minecraft/textures/items/iron_chestplate',
        'assets/minecraft/textures/items/iron_leggings',
        'assets/minecraft/textures/items/iron_boots',
        'assets/minecraft/textures/items/golden_helmet',
        'assets/minecraft/textures/items/golden_chestplate',
        'assets/minecraft/textures/items/golden_leggings',
        'assets/minecraft/textures/items/golden_boots',
        'assets/minecraft/textures/items/diamond_helmet',
        'assets/minecraft/textures/items/diamond_chestplate',
        'assets/minecraft/textures/items/diamond_leggings',
        'assets/minecraft/textures/items/diamond_boots',
        'assets/minecraft/textures/items/chainmail_helmet',
        'assets/minecraft/textures/items/chainmail_chestplate',
        'assets/minecraft/textures/items/chainmail_leggings',
        'assets/minecraft/textures/items/chainmail_boots'
    ],
    'buckets': [
        'assets/minecraft/textures/items/bucket_empty',
        'assets/minecraft/textures/items/bucket_lava',
        'assets/minecraft/textures/items/bucket_milk',
        'assets/minecraft/textures/items/bucket_water'
    ],
    'endstone': [
        'assets/minecraft/textures/blocks/end_stone'
    ],
    'wood': [
        'assets/minecraft/textures/blocks/planks_oak',
        'assets/minecraft/textures/blocks/planks_spruce',
        'assets/minecraft/textures/blocks/planks_birch',
        'assets/minecraft/textures/blocks/planks_jungle',
        'assets/minecraft/textures/blocks/planks_acacia',
        'assets/minecraft/textures/blocks/planks_dark_oak',
        'assets/minecraft/textures/blocks/planks_big_oak',
        'assets/minecraft/textures/blocks/log_acacia',
        'assets/minecraft/textures/blocks/log_acacia_top',
        'assets/minecraft/textures/blocks/log_big_oak',
        'assets/minecraft/textures/blocks/log_big_oak_top',
        'assets/minecraft/textures/blocks/log_birch',
        'assets/minecraft/textures/blocks/log_birch_top',
        'assets/minecraft/textures/blocks/log_jungle',
        'assets/minecraft/textures/blocks/log_jungle_top',
        'assets/minecraft/textures/blocks/log_oak',
        'assets/minecraft/textures/blocks/log_oak_top',
        'assets/minecraft/textures/blocks/log_spruce',
        'assets/minecraft/textures/blocks/log_spruce_top',
    ],
    'ladder': [
        'assets/minecraft/textures/blocks/ladder'
        #'assets/minecraft/models/block/ladder.json'
    ],
    'obsidian': [
        'assets/minecraft/textures/blocks/obsidian'
    ],
    'sword': [
        'assets/minecraft/textures/items/wooden_sword',
        'assets/minecraft/textures/items/stone_sword',
        'assets/minecraft/textures/items/iron_sword',
        'assets/minecraft/textures/items/golden_sword',
        'assets/minecraft/textures/items/diamond_sword'
    ],
    'stick': [
        'assets/minecraft/textures/items/stick' 
    ],
    'armour-model': [
        'assets/minecraft/textures/models/armor/leather_layer_1_overlay',
        'assets/minecraft/textures/models/armor/leather_layer_1',
        'assets/minecraft/textures/models/armor/leather_layer_2_overlay',
        'assets/minecraft/textures/models/armor/leather_layer_2',
        'assets/minecraft/textures/models/armor/iron_layer_1_overlay',
        'assets/minecraft/textures/models/armor/iron_layer_1',
        'assets/minecraft/textures/models/armor/iron_layer_2_overlay',
        'assets/minecraft/textures/models/armor/iron_layer_2',
        'assets/minecraft/textures/models/armor/gold_layer_1_overlay',
        'assets/minecraft/textures/models/armor/gold_layer_1',
        'assets/minecraft/textures/models/armor/gold_layer_2_overlay',
        'assets/minecraft/textures/models/armor/gold_layer_2',
        'assets/minecraft/textures/models/armor/diamond_layer_1_overlay',
        'assets/minecraft/textures/models/armor/diamond_layer_1',
        'assets/minecraft/textures/models/armor/diamond_layer_2_overlay',
        'assets/minecraft/textures/models/armor/diamond_layer_2',
        'assets/minecraft/textures/models/armor/chainmail_layer_1_overlay',
        'assets/minecraft/textures/models/armor/chainmail_layer_1',
        'assets/minecraft/textures/models/armor/chainmail_layer_2_overlay',
        'assets/minecraft/textures/models/armor/chainmail_layer_2'
    ],
    'tools': [
        'assets/minecraft/textures/items/wooden_pickaxe',
        'assets/minecraft/textures/items/wooden_axe',
        'assets/minecraft/textures/items/wooden_shovel',
        'assets/minecraft/textures/items/wooden_hoe',
        'assets/minecraft/textures/items/stone_pickaxe',
        'assets/minecraft/textures/items/stone_axe',
        'assets/minecraft/textures/items/stone_shovel',
        'assets/minecraft/textures/items/stone_hoe',
        'assets/minecraft/textures/items/iron_pickaxe',
        'assets/minecraft/textures/items/iron_axe',
        'assets/minecraft/textures/items/iron_shovel',
        'assets/minecraft/textures/items/iron_hoe',
        'assets/minecraft/textures/items/golden_pickaxe',
        'assets/minecraft/textures/items/golden_axe',
        'assets/minecraft/textures/items/golden_shovel',
        'assets/minecraft/textures/items/golden_hoe',
        'assets/minecraft/textures/items/diamond_pickaxe',
        'assets/minecraft/textures/items/diamond_axe',
        'assets/minecraft/textures/items/diamond_shovel',
        'assets/minecraft/textures/items/diamond_hoe'
    ],
    'shears': [
        'assets/minecraft/textures/items/shears'
    ],
    'arrow': [
        'assets/minecraft/textures/items/arrow'
    ],
    'potions': [
        'assets/minecraft/textures/items/potion_bottle_drinkable',
        'assets/minecraft/textures/items/potion_bottle_splash',
        'assets/minecraft/textures/items/potion_overlay',
        'assets/minecraft/textures/items/potion_bottle_empty',
    ],
    'projectile': [
        'assets/minecraft/textures/items/egg',
        'assets/minecraft/textures/items/snowball',
    ],
    'pearl': [
        'assets/minecraft/textures/items/ender_pearl',
    ],
    'gui': [
        'assets/minecraft/textures/gui/container/inventory',
        'assets/minecraft/textures/gui/container/creative_inventory/tab_items',
        'assets/minecraft/textures/gui/container/creative_inventory/tab_inventory',
        'assets/minecraft/textures/gui/container/creative_inventory/tab_search',
        'assets/minecraft/textures/gui/container/creative_inventory/tab_favorites',
        'assets/minecraft/textures/gui/container/creative_inventory/tab_decorations',
        'assets/minecraft/textures/gui/container/creative_inventory/tab_redstone',
        'assets/minecraft/textures/gui/container/creative_inventory/tab_tools',
        'assets/minecraft/textures/gui/container/creative_inventory/tab_food',
        'assets/minecraft/textures/gui/container/creative_inventory/tab_blocks',
        'assets/minecraft/textures/gui/container/creative_inventory/tab_transportation',
        'assets/minecraft/textures/gui/container/creative_inventory/tab_misc',
        'assets/minecraft/textures/gui/container/creative_inventory/tab_inventory',
        'assets/minecraft/textures/gui/container/generic_54',
        'assets/minecraft/textures/gui/container/hopper',
        'assets/minecraft/textures/gui/container/furnace',
        'assets/minecraft/textures/gui/container/brewing_stand',
        'assets/minecraft/textures/gui/icons',
        'assets/minecraft/textures/gui/options_background',
    ],
    'fireball': [
        'assets/minecraft/textures/items/fireball',
    ],
    'tnt': [
        'assets/minecraft/textures/blocks/tnt_top',
        'assets/minecraft/textures/blocks/tnt_side',
        'assets/minecraft/textures/blocks/tnt_bottom',
    ],
    'sponge': [
        'assets/minecraft/textures/blocks/sponge',
    ],
    'chest': [
        'assets/minecraft/textures/entity/chest/christmas',
        'assets/minecraft/textures/entity/chest/christmas_double',
        'assets/minecraft/textures/entity/chest/christmas_left',
        'assets/minecraft/textures/entity/chest/christmas_right',
        'assets/minecraft/textures/entity/chest/normal',
        'assets/minecraft/textures/entity/chest/normal_double',
        'assets/minecraft/textures/entity/chest/normal_left',
        'assets/minecraft/textures/entity/chest/normal_right',
        'assets/minecraft/textures/entity/chest/trapped',
        'assets/minecraft/textures/entity/chest/trapped_double',
        'assets/minecraft/textures/entity/chest/trapped_left',
        'assets/minecraft/textures/entity/chest/trapped_right',
        'assets/minecraft/textures/entity/chest/ender',
    ],
    'fishing-rod': [
        'assets/minecraft/textures/items/fishing_rod_cast',
        'assets/minecraft/textures/items/fishing_rod_uncast',
    ],
    'sandstone': [
        'assets/minecraft/textures/blocks/sandstone_top',
        'assets/minecraft/textures/blocks/sandstone_bottom',
        'assets/minecraft/textures/blocks/sandstone_normal',
        'assets/minecraft/textures/blocks/sandstone_carved',
        'assets/minecraft/textures/blocks/sandstone_smooth',
    ],
    'resource-items':[
        'assets/minecraft/textures/items/coal',
        'assets/minecraft/textures/items/iron_ingot',
        'assets/minecraft/textures/items/gold_ingot',
        'assets/minecraft/textures/items/diamond',
        'assets/minecraft/textures/items/emerald',
        'assets/minecraft/textures/items/lapis_lazuli',
        'assets/minecraft/textures/items/redstone',
        'assets/minecraft/textures/items/quartz',
    ],
    'resource-blocks': [
        'assets/minecraft/textures/blocks/coal_block',
        'assets/minecraft/textures/blocks/iron_block',
        'assets/minecraft/textures/blocks/gold_block',
        'assets/minecraft/textures/blocks/diamond_block',
        'assets/minecraft/textures/blocks/emerald_block',
        'assets/minecraft/textures/blocks/lapis_block',
        'assets/minecraft/textures/blocks/redstone_block',
        'assets/minecraft/textures/blocks/quartz_block',
        'assets/minecraft/textures/blocks/quartz_block_chiseled',
        'assets/minecraft/textures/blocks/quartz_block_lines',
        'assets/minecraft/textures/blocks/quartz_block_side',
        'assets/minecraft/textures/blocks/quartz_block_top',
        'assets/minecraft/textures/blocks/quartz_ore',
    ],
    'ore-blocks': [
        'assets/minecraft/textures/blocks/coal_ore',
        'assets/minecraft/textures/blocks/iron_ore',
        'assets/minecraft/textures/blocks/gold_ore',
        'assets/minecraft/textures/blocks/diamond_ore',
        'assets/minecraft/textures/blocks/emerald_ore',
        'assets/minecraft/textures/blocks/lapis_ore',
        'assets/minecraft/textures/blocks/redstone_ore',
        'assets/minecraft/textures/blocks/quartz_ore',   
    ],
    'eye-of-ender': [
        'assets/minecraft/textures/items/ender_eye',
    ],
    'ice': [
        'assets/minecraft/textures/blocks/ice',
        'assets/minecraft/textures/blocks/packed_ice',
    ],
    'breaking-animation': [
        'assets/minecraft/textures/blocks/destroy_stage_0',
        'assets/minecraft/textures/blocks/destroy_stage_1',
        'assets/minecraft/textures/blocks/destroy_stage_2',
        'assets/minecraft/textures/blocks/destroy_stage_3',
        'assets/minecraft/textures/blocks/destroy_stage_4',
        'assets/minecraft/textures/blocks/destroy_stage_5',
        'assets/minecraft/textures/blocks/destroy_stage_6',
        'assets/minecraft/textures/blocks/destroy_stage_7',
        'assets/minecraft/textures/blocks/destroy_stage_8',
        'assets/minecraft/textures/blocks/destroy_stage_9',
    ],
    'bed': [
        'assets/minecraft/textures/items/bed',
        'assets/minecraft/textures/blocks/bed_feet_top',
        'assets/minecraft/textures/blocks/bed_feet_end',
        'assets/minecraft/textures/blocks/bed_feet_side',
        'assets/minecraft/textures/blocks/bed_head_top',
        'assets/minecraft/textures/blocks/bed_head_end',
        'assets/minecraft/textures/blocks/bed_head_side',
    ],
    'glass': [
        'assets/minecraft/textures/blocks/glass_black',
        'assets/minecraft/textures/blocks/glass',
        'assets/minecraft/textures/blocks/glass_blue',
        'assets/minecraft/textures/blocks/glass_brown',
        'assets/minecraft/textures/blocks/glass_cyan',
        'assets/minecraft/textures/blocks/glass_gray',
        'assets/minecraft/textures/blocks/glass_green',
        'assets/minecraft/textures/blocks/glass_light_blue',
        'assets/minecraft/textures/blocks/glass_lime',
        'assets/minecraft/textures/blocks/glass_magenta',
        'assets/minecraft/textures/blocks/glass_orange',
        'assets/minecraft/textures/blocks/glass_silver',
        'assets/minecraft/textures/blocks/glass_pink',
        'assets/minecraft/textures/blocks/glass_purple',
        'assets/minecraft/textures/blocks/glass_red',
        'assets/minecraft/textures/blocks/glass_white',
        'assets/minecraft/textures/blocks/glass_yellow',
    ]
}

    #make credits
    

if not os.path.exists('temp/'):
    unzip(args.input)
    remove_extra()

if not os.path.exists('output/'):
    os.makedirs('output/')
if not os.path.exists(f'output/assets/minecraft/textures/blocks'):
    os.makedirs(f'output/assets/minecraft/textures/blocks')
if not os.path.exists(f'output/assets/minecraft/textures/items'):
    os.makedirs(f'output/assets/minecraft/textures/items')
if not os.path.exists(f'output/assets/minecraft/textures/models/block'):
    os.makedirs(f'output/assets/minecraft/textures/models/block')
if not os.path.exists(f'output/assets/minecraft/models/block'):
    os.makedirs(f'output/assets/minecraft/models/block')
if not os.path.exists(f'output/assets/minecraft/textures/entity/chest'):
    os.makedirs(f'output/assets/minecraft/textures/entity/chest')
if not os.path.exists(f'output/assets/minecraft/textures/models/armor'):
    os.makedirs(f'output/assets/minecraft/textures/models/armor')
if not os.path.exists(f'output/assets/minecraft/textures/gui/container/creative_inventory'):
    os.makedirs(f'output/assets/minecraft/textures/gui/container/creative_inventory')
if not os.path.exists('preview/'):
    os.makedirs('preview/')

packs = os.listdir('temp/')

packs.sort()

if args.name != None:
    name = args.name
else:
    name = input('Pack Name: ')

if args.description != None:
    description = args.description
else:
    description = input('Pack Description: ')

with open ('output/pack.mcmeta', 'w') as f:
    f.write(json.dumps({
        'pack': {
            'pack_format': 1,
            'description': description
        }
    }, indent=4))

    #create an atlas of the images in each option from each pack, and let the user select which pack they want to extract from

if not args.disable_preview_gen:
    previewStart = time.time()
    preview = {}
    for o in options:
        o2 = options[o]
        temp = {}
        for option in o2:
            for pack in packs:
                if option.endswith('.json'):
                    path = f'temp/{pack}/{option}'
                else:
                    path = f'temp/{pack}/{option}.png'

                if os.path.exists(path):
                    if pack not in temp:
                        temp[pack] = []
                    temp[pack].append(Image.open(path))
            #merge the images into one big image
        if temp.__len__() > 0:
            for pack in temp:
                image = Image.new('RGBA', (temp[pack][0].width * temp[pack].__len__(), temp[pack][0].height))
                for i in range(temp[pack].__len__()):
                    #check if the file's name contains overlay
                    if 'overlay' not in temp[pack][i].filename and 'creative_inventory' not in temp[pack][i].filename:
                        #i know it's a nested if,  but it looks nicer
                        #generic_54, hopper, furnace brewing stand
                        if 'furnace' not in temp[pack][i].filename and 'brewing_stand' not in temp[pack][i].filename and 'hopper' not in temp[pack][i].filename and 'generic_54' not in temp[pack][i].filename:
                            image.paste(temp[pack][i], (temp[pack][i].width * i, 0))
                temp[pack] = image
                print(f'Preview image created for {o} from {pack}')
                temp[pack].save(f'preview/{o}_{pack}.png')
        preview[o] = temp
    print(f'Preview images created in {time.time() - previewStart} seconds')

choices = {}

app = Flask(__name__, template_folder='templates')
i = 0
o = []
for q in options:
    o.append(q)
queue = []
for pack in packs:
    path = f'{o[i]}_{pack}.png'
    queue.append(path)

completed = False

def assemble_pack():
    global completed
    print('Assembling pack...')
    print(options)
    print(choices)
    for o in options:
        if o in choices:
            choice = choices[o]
            print(choice)
            for option in options[o]:
                print(option)
                #check if the folder exists
                packname = choice['pack'].replace('.png','')
                if os.path.exists(f'temp/{packname}/{option}.png'):
                    print(f'temp/{packname}/{option}.png')
                    shutil.copyfile(f'temp/{packname}/{option}.png', f'output/{option}.png')
                    if o == 'ladder':
                        #'assets/minecraft/models/block/ladder.json'
                        if os.path.exists(f'temp/{packname}/assets/minecraft/models/block/ladder.json'):
                            shutil.copyfile(f'temp/{packname}/assets/minecraft/models/block/ladder.json', f'output/assets/minecraft/models/block/ladder.json')

                if os.path.exists(f'temp/{packname}/{option}.mcmeta'):
                    shutil.copyfile(f'temp/{packname}/{option}.mcmeta', f'output/assets/minecraft/textures/{option}.mcmeta')
    if args.no_credits:
        with open('output/credits.txt', 'w', encoding='utf-8') as f:
            for choice in choices:
                packname = choices[choice]['pack'].replace('.png','')
                f.write(f'{choice.title()}: {packname}\n')
    print('Pack assembled')
    print('Zipping...')
    for file in os.listdir('output'):
        if file.endswith('.zip'):
            os.remove(f'output/{file}')
    shutil.make_archive(f'output/{name}', 'zip', 'output')
    print('Zipped')
    completed = True
    print('You can now close the program, by either closing the terminal or using Ctrl+C')


print('Starting server...')
@app.route('/')
def index():
    return render_template('images.html', dict={
        "queue": [[x,j, x.split("_")[1]] for j,x in enumerate(queue)],
        "type": o[i],
    })
@app.route('/select', methods=['POST'])
def select():
    global i
    global queue
    print('Selecting...')
    selected = int(request.json['number'])
    try:
        choices[o[i]] = {
            'id': selected,
            'pack': queue[selected].split("_")[1]
        }
    except IndexError:
        i-=2

    i+=1
    if i >= o.__len__():
        print('Done')
        assemble_pack()
        return jsonify({'m':True}), 200

    queue = []
    for pack in packs:
        path = f'{o[i]}_{pack}.png'
        queue.append(path)
    print(choices)
    return jsonify({'m':False}), 200
@app.route('/image/<path:path>')
def send_image(path):
    return send_from_directory('preview', path)
@app.route('/status')
def status():
    return jsonify({
        'status': completed
    })
@app.route('/complete')
def complete():
    return render_template('complete.html', dict={
        'path': f'output/{name}.zip'
    })
print("""----------------------------------------
Server started, go to http://localhost:5000 to choose your options
----------------------------------------""")
app.run('localhost', 5000)
        
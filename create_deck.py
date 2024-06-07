from PIL import Image, ImageDraw, ImageFont
import os
import json
import math
import itertools

vert_card_dim = Image.open("card_data/sorcerycardmagic.png").size

set_name = "trump set"
deck_name = "littlemorebalanced"
set_dir = f"card_data/{set_name}"

save_dir = f"created_decks/{set_name}/{deck_name}"

if __name__ == "__main__":
    if not os.path.isdir(set_dir):
        print(f"Set does not exist: {set_dir}")
        exit()

    os.makedirs(save_dir, exist_ok=True)

    card_data = {}
    with open(f"{set_dir}/card_data.json") as card_json:
        card_data = json.load(card_json)

    deck = card_data["decks"][deck_name]

    avatar_card = Image.open(f"{set_dir}/rendered_cards/{deck['avatar']}.png")
    avatar_card.save(f"{save_dir}/avatar.png")

    atlas = deck["atlas"]
    atlas_sheet_dims = [
        math.floor(math.sqrt(len(atlas))),
        math.ceil(len(atlas) / math.floor(math.sqrt(len(atlas)))),
    ]

    spellbook = deck["spellbook"]
    spellbook_sheet_dims = [
        math.floor(math.sqrt(len(spellbook))),
        math.ceil(len(spellbook) / math.floor(math.sqrt(len(spellbook)))),
    ]

    spellcard_size = Image.open("card_data/sorcerycardmagic.png").size
    sitecard_size = Image.open("card_data/sorcerycardsite.png").size

    atlas_sheet = Image.new(
        "RGBA",
        [
            atlas_sheet_dims[0] * sitecard_size[0],
            atlas_sheet_dims[1] * sitecard_size[1],
        ],
        (0, 0, 0, 0),
    )
    spellbook_sheet = Image.new(
        "RGBA",
        [
            spellbook_sheet_dims[0] * spellcard_size[0],
            spellbook_sheet_dims[1] * spellcard_size[1],
        ],
        (0, 0, 0, 0),
    )

    atlas_sheet_coords = list(
        itertools.product(range(atlas_sheet_dims[1]), range(atlas_sheet_dims[0]))
    )[: len(atlas)]
    for i, coord in enumerate(atlas_sheet_coords):
        card_img = Image.open(f"{set_dir}/rendered_cards/{atlas[i]}.png")
        atlas_sheet.paste(
            card_img, [coord[1] * sitecard_size[0], coord[0] * sitecard_size[1]]
        )

    spellbook_sheet_coords = list(
        itertools.product(
            range(spellbook_sheet_dims[1]), range(spellbook_sheet_dims[0])
        )
    )[: len(spellbook)]
    for i, coord in enumerate(spellbook_sheet_coords):
        card_img = Image.open(f"{set_dir}/rendered_cards/{spellbook[i]}.png")
        spellbook_sheet.paste(
            card_img, [coord[1] * spellcard_size[0], coord[0] * spellcard_size[1]]
        )

    atlas_sheet.save(
        f"{save_dir}/atlas_{atlas_sheet_dims[0]}x{atlas_sheet_dims[1]}_{len(atlas)}.png"
    )
    spellbook_sheet.save(
        f"{save_dir}/spellbook_{spellbook_sheet_dims[0]}x{spellbook_sheet_dims[1]}_{len(spellbook)}.png"
    )

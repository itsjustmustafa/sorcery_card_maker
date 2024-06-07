from PIL import Image, ImageOps
import os
import json

vert_card_dim = Image.open("sorcerycardmagic.png").size

set_name = "trump set"

set_dir = f"card_data/{set_name}"
if __name__ == "__main__":
    if not os.path.isdir(set_dir):
        print(f"Set does not exist: {set_dir}")
        exit()

    card_data = {}
    with open(f"{set_dir}/card_data.json") as card_json:
        card_data = json.load(card_json)

    vert_cards = []
    horz_cards = []

    # vert_cardis.append(card_data["avatar"]["name"])

    for avatar_card in card_data["avatar"]:
        vert_cards.append(avatar_card["name"])

    for magic_card in card_data["magic"]:
        vert_cards.append(magic_card["name"])

    for minion_card in card_data["minion"]:
        vert_cards.append(minion_card["name"])

    for site_card in card_data["site"]:
        horz_cards.append(site_card["name"])

    # print(vert_cards)
    # print(horz_cards)

    if not os.path.isdir(f"{set_dir}/resized_images"):
        os.mkdir(f"{set_dir}/resized_images")
    for vert_card_name in vert_cards:
        bg_image = ImageOps.fit(
            Image.open(f"{set_dir}/images/{vert_card_name}.png"), vert_card_dim
        ).save(f"{set_dir}/resized_images/{vert_card_name}.png", "PNG")
    for horz_card_name in horz_cards:
        bg_image = ImageOps.fit(
            Image.open(f"{set_dir}/images/{horz_card_name}.png"), vert_card_dim[::-1]
        ).save(f"{set_dir}/resized_images/{horz_card_name}.png")

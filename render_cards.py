from PIL import Image, ImageDraw, ImageFont
import os
import json

vert_card_dim = Image.open("card_data/sorcerycardmagic.png").size

set_name = "trump set"

set_dir = f"card_data/{set_name}"


def contrastText(draw, *args, **kwargs):
    draw.text(*args, fill=(255, 255, 255), **kwargs, stroke_width=2)
    draw.text(*args, fill=(0, 0, 0), **kwargs)


def bestFontSize(text_length):
    biggest_size = 20
    least_filled_length = 32
    return biggest_size * least_filled_length / max(text_length, least_filled_length)


if __name__ == "__main__":
    if not os.path.isdir(set_dir):
        print(f"Set does not exist: {set_dir}")
        exit()

    if not os.path.isdir(f"{set_dir}/rendered_cards"):
        os.mkdir(f"{set_dir}/rendered_cards")

    card_data = {}
    with open(f"{set_dir}/card_data.json") as card_json:
        card_data = json.load(card_json)

    top_font = ImageFont.truetype("ComicMono.ttf", 27)
    bottom_font = ImageFont.truetype("ComicMono.ttf", 15)

    for avatar_card_data in card_data["avatar"]:
        avatar_bg = Image.open(
            f"{set_dir}/resized_images/{avatar_card_data['name']}.png"
        ).convert("RGBA")
        avatar_rendered = Image.alpha_composite(
            avatar_bg, Image.open("card_data/sorcerycardavatar.png").convert("RGBA")
        )
        draw = ImageDraw.Draw(avatar_rendered)

        contrastText(
            draw,
            [vert_card_dim[0] / 2, 40],
            avatar_card_data["name"],
            font=top_font,
            anchor="mm",
        )
        contrastText(
            draw,
            [63, 40],
            str(avatar_card_data["starting_life"]),
            font=top_font,
            anchor="mm",
        )
        contrastText(
            draw,
            [vert_card_dim[0] - 63, 40],
            str(avatar_card_data["attack"]),
            font=top_font,
            anchor="mm",
        )

        flavour_font = ImageFont.truetype(
            "ComicMono.ttf", bestFontSize(len(avatar_card_data["flavour"]))
        )
        contrastText(
            draw, [46, 470], avatar_card_data["flavour"], font=flavour_font, anchor="lm"
        )

        for i, line in enumerate(avatar_card_data["text"]):
            contrastText(draw, [50, 500 + 20 * i], line, font=bottom_font, anchor="lm")

        avatar_rendered.save(f"{set_dir}/rendered_cards/{avatar_card_data['name']}.png")

    for magic_card_data in card_data["magic"]:
        card_bg = Image.open(
            f"{set_dir}/resized_images/{magic_card_data['name']}.png"
        ).convert("RGBA")
        card_rendered = Image.alpha_composite(
            card_bg, Image.open("card_data/sorcerycardmagic.png")
        ).convert("RGBA")
        draw = ImageDraw.Draw(card_rendered)
        contrastText(
            draw, [51, 41], str(magic_card_data["mana"]), font=top_font, anchor="mm"
        )

        contrastText(
            draw,
            [vert_card_dim[0] / 2, 41],
            magic_card_data["name"],
            font=top_font,
            anchor="mm",
        )
        for i, line in enumerate(magic_card_data["text"]):
            contrastText(draw, [50, 500 + 20 * i], line, font=bottom_font, anchor="lm")

        card_rendered.save(f"{set_dir}/rendered_cards/{magic_card_data['name']}.png")

    for minion_card_data in card_data["minion"]:
        card_bg = Image.open(
            f"{set_dir}/resized_images/{minion_card_data['name']}.png"
        ).convert("RGBA")
        card_rendered = Image.alpha_composite(
            card_bg, Image.open("card_data/sorcerycardminion.png")
        ).convert("RGBA")
        draw = ImageDraw.Draw(card_rendered)

        contrastText(
            draw,
            [51, 41],
            str(minion_card_data["mana"]),
            font=top_font,
            anchor="mm",
        )
        contrastText(
            draw,
            [vert_card_dim[0] - 51, 41],
            str(minion_card_data["power"]),
            font=top_font,
            anchor="mm",
        )

        contrastText(
            draw,
            [vert_card_dim[0] / 2, 41],
            minion_card_data["name"],
            font=top_font,
            anchor="mm",
        )
        for i, line in enumerate(minion_card_data["text"]):
            contrastText(draw, [50, 500 + 20 * i], line, font=bottom_font, anchor="lm")

        card_rendered.save(f"{set_dir}/rendered_cards/{minion_card_data['name']}.png")

    for site_card_data in card_data["site"]:
        card_bg = Image.open(
            f"{set_dir}/resized_images/{site_card_data['name']}.png"
        ).convert("RGBA")
        card_rendered = Image.alpha_composite(
            card_bg, Image.open("card_data/sorcerycardsite.png")
        ).convert("RGBA")
        draw = ImageDraw.Draw(card_rendered)

        contrastText(
            draw, [70, 340], site_card_data["name"], font=bottom_font, anchor="lm"
        )
        for i, line in enumerate(site_card_data["text"]):
            contrastText(draw, [70, 367 + 20 * i], line, font=bottom_font, anchor="lm")

        card_rendered.save(f"{set_dir}/rendered_cards/{site_card_data['name']}.png")

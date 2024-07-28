from PIL import Image, ImageDraw, ImageFont
import os
import json
from typing import List

vert_card_dim = Image.open("sorcerycardmagic.png").size

set_name = "trump set"

set_dir = f"card_data/{set_name}"

TEXT_LINE_HEIGHT = 20
VERTICAL_CARD_TEXT_COORDS = [50, 497]
MANA_COORDS = [51, 41]
POWER_COORDS = [399, 41]
NAME_COORDS = [225, 41]
AVATAR_NAME_COORDS = [225, 40]
AVATAR_LIFE_COORDS = [63, 40]
AVATAR_ATTACK_COORDS = [387, 40]
TYPELINE_TEXT_COORDS = [46, 470]


def contrastText(draw, *args, **kwargs):
    draw.text(*args, fill=(255, 255, 255), **kwargs, stroke_width=3)
    draw.text(*args, fill=(0, 0, 0), **kwargs)


def bestFontSize(text_length):
    biggest_size = 20
    least_filled_length = 32
    return biggest_size * least_filled_length / max(text_length, least_filled_length)


def getLinesFromText(text: str, max_line_length: int):
    all_lines = []
    for delimited_text in text.split("\n"):
        delimited_text = delimited_text.strip()
        words = delimited_text.split()
        lines = [words[0]]
        for word in words[1:]:
            rendered_word = word
            match word:
                case "->":
                    rendered_word = "→"
                case "(1)":
                    rendered_word = "⑴"
                case "(2)":
                    rendered_word = "⑵"
                case "(3)":
                    rendered_word = "⑶"
                case "(4)":
                    rendered_word = "⑷"
                case "(5)":
                    rendered_word = "⑸"
                case "(6)":
                    rendered_word = "⑹"
                case "(7)":
                    rendered_word = "⑺"
                case "(8)":
                    rendered_word = "⑻"
                case "(9)":
                    rendered_word = "⑼"

            if len(lines[-1] + " " + rendered_word) <= max_line_length:
                lines[-1] += " " + rendered_word
            else:
                lines.append(rendered_word)
        all_lines.extend(lines)
    return all_lines


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
            avatar_bg, Image.open("sorcerycardavatar.png").convert("RGBA")
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

        typeline_font = ImageFont.truetype(
            "ComicMono.ttf", bestFontSize(len(avatar_card_data["typeline"]))
        )
        contrastText(
            draw,
            [46, 470],
            avatar_card_data["typeline"],
            font=typeline_font,
            anchor="lm",
        )

        max_line_length = 42
        lines_of_text = getLinesFromText(avatar_card_data["text"], max_line_length)
        for i, line in enumerate(lines_of_text):
            contrastText(
                draw,
                [
                    VERTICAL_CARD_TEXT_COORDS[0],
                    VERTICAL_CARD_TEXT_COORDS[1] + TEXT_LINE_HEIGHT * i,
                ],
                line,
                font=bottom_font,
                anchor="lm",
            )

        avatar_rendered.save(f"{set_dir}/rendered_cards/{avatar_card_data['name']}.png")

    for magic_card_data in card_data["magic"]:
        card_bg = Image.open(
            f"{set_dir}/resized_images/{magic_card_data['name']}.png"
        ).convert("RGBA")
        card_rendered = Image.alpha_composite(
            card_bg, Image.open("sorcerycardmagic.png")
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
        max_line_length = 42
        lines_of_text = getLinesFromText(magic_card_data["text"], max_line_length)
        for i, line in enumerate(lines_of_text):
            contrastText(
                draw,
                [
                    VERTICAL_CARD_TEXT_COORDS[0],
                    VERTICAL_CARD_TEXT_COORDS[1] + TEXT_LINE_HEIGHT * i,
                ],
                line,
                font=bottom_font,
                anchor="lm",
            )

        card_rendered.save(f"{set_dir}/rendered_cards/{magic_card_data['name']}.png")

    for minion_card_data in card_data["minion"]:
        card_bg = Image.open(
            f"{set_dir}/resized_images/{minion_card_data['name']}.png"
        ).convert("RGBA")
        card_rendered = Image.alpha_composite(
            card_bg, Image.open("sorcerycardminion.png")
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
        max_line_length = 42
        lines_of_text = getLinesFromText(minion_card_data["text"], max_line_length)
        for i, line in enumerate(lines_of_text):
            contrastText(
                [
                    VERTICAL_CARD_TEXT_COORDS[0],
                    VERTICAL_CARD_TEXT_COORDS[1] + TEXT_LINE_HEIGHT * i,
                ],
                line,
                font=bottom_font,
                anchor="lm",
            )

        card_rendered.save(f"{set_dir}/rendered_cards/{minion_card_data['name']}.png")

    for site_card_data in card_data["site"]:
        card_bg = Image.open(
            f"{set_dir}/resized_images/{site_card_data['name']}.png"
        ).convert("RGBA")
        card_rendered = Image.alpha_composite(
            card_bg, Image.open("sorcerycardsite.png")
        ).convert("RGBA")
        draw = ImageDraw.Draw(card_rendered)

        contrastText(
            draw, [70, 340], site_card_data["name"], font=bottom_font, anchor="lm"
        )
        max_line_length = 60
        lines_of_text = getLinesFromText(site_card_data["text"], max_line_length)
        for i, line in enumerate(lines_of_text):
            contrastText(draw, [70, 367 + 20 * i], line, font=bottom_font, anchor="lm")

        card_rendered.save(f"{set_dir}/rendered_cards/{site_card_data['name']}.png")

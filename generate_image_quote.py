from PIL import Image, ImageDraw, ImageFont
import textwrap


def quote_on_image(row_quote, img, font):
    quote = row_quote["Pic"].strip()

    para = textwrap.wrap(quote, width=32)
    MAX_W, MAX_H = img.size
    draw = ImageDraw.Draw(img)

    text_h = draw.textsize(para[0], font=font)[1] * len(para)
    padding = 20
    starting_h = ((MAX_H - text_h) + ((len(para) - 1) * padding)) / 2

    for line in para:
        w, h = draw.textsize(line, font=font)
        draw.text(((MAX_W - w) / 2, starting_h), line, (0, 0, 0), font=font)
        starting_h += h + padding

    if row_quote["direct quote"] == "Yes" and (
        row_quote["Reference"] != "Maria" or row_quote["Reference"] != "Ben's notes"
    ):
        direct_font = ImageFont.truetype(
            "/System/Library/Fonts/Supplemental/Andale Mono.ttf", 70
        )
        w, h = draw.textsize(row_quote["Reference"], font=direct_font)
        draw.text(
            ((MAX_W - w) / 2, starting_h + 3 * padding),
            f"by {row_quote['Reference']}",
            (0, 0, 0),
            font=direct_font,
        )
    return img


def generate_image(quote):
    img = Image.open("quotes/background/deep_dreath_crop.png")
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Andale Mono.ttf", 135)

    img = Image.open("quotes/background/deep_dreath_crop.png")
    img = quote_on_image(quote, img, font)
    return img


def generate_and_get_image_path(quote):
    path_to_save = f"quotes/images/img_quote_{quote.index[0]}.png"
    img = generate_image(quote.iloc[0])
    img.save(path_to_save)
    return path_to_save

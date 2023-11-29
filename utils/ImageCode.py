from PIL import Image, ImageDraw, ImageFont
from random import randint, choice
from string import ascii_uppercase, digits


def generate_image_code(image_size=(150, 35), code_length=5, font_file='utils/segoepr.ttf', font_size=28):
    img = Image.new('RGB', image_size, 'grey')
    draw = ImageDraw.Draw(img, 'RGB')

    # Generate image code.
    code = ''
    font = ImageFont.truetype(font_file, font_size)
    for i in range(code_length):
        char = random_char()
        code = code + char
        x = i * image_size[0] / code_length
        y = -10
        draw.text((x, y), char, fill=random_color(), font=font)

    # Add confusing elements.
    for i in range(100):
        x = randint(0, image_size[0])
        y = randint(0, image_size[1])
        draw.point((x, y), fill=random_color())

    for i in range(10):
        x1 = randint(0, image_size[0])
        y1 = randint(0, image_size[1])
        x2 = randint(0, image_size[0])
        y2 = randint(0, image_size[1])
        draw.line((x1, y1, x2, y2), fill=random_color())

    return img, code


def random_char():
    char = choice(ascii_uppercase + digits)
    return char


def random_color():
    red = randint(0, 255)
    green = randint(0, 255)
    blue = randint(0, 255)
    color = (red, green, blue)
    return color


from pexels_api import API
import urllib.request
import numpy as np
import pandas as pd
import cv2
import random
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import textwrap
import random

def image_retrieve(keyword, id):
# featuers: list
    PEXELS_API_KEY = '563492ad6f91700001000001640062542b4143a48056ff5355a3ced8'
    IMAGE_PATH = 'photos/%s.jpeg' % id
    api = API(PEXELS_API_KEY)

    api.search(keyword, results_per_page=5, page=2)

    photos = api.get_entries()

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)

    photo = random.choice(photos)

    image = urllib.request.urlretrieve(photo.original, IMAGE_PATH)

    return IMAGE_PATH

def image_filter(image_path, id):
    image_path_list = image_path.split('.')
    image_path_list[0] += '_processed'
    image_path_save = '.'.join(image_path_list)
    # set colours (BGR)
    background_colour = [203,172,159]
    dots_colour = (102, 20, 7)

    # set the max dots (on the longest side of the image)
    max_dots = 100

    # import the image as greyscale
    original_image = cv2.imread(image_path, 0)

    # extract dimensions
    original_image_height, original_image_width = original_image.shape

    # down size to number of dots
    if original_image_width == max(original_image_height,original_image_width):
        downsized_image = cv2.resize(original_image,(int(original_image_height*(max_dots/original_image_width)),max_dots))
    else:
        downsized_image = cv2.resize(original_image,(max_dots,int(original_image_height*(max_dots/original_image_width))))

    # extract dimensions of new image
    downsized_image_height, downsized_image_width = downsized_image.shape

    # set how big we want our final image to be
    multiplier = 100

    # set the size of our blank canvas
    blank_img_height = downsized_image_height * multiplier
    blank_img_width = downsized_image_width * multiplier

    # set the padding value so the dots start in frame (rather than being off the edge
    padding = int(multiplier/2)

    # create canvas containing just the background colour
    blank_image = np.full(((blank_img_height),(blank_img_width),3), background_colour,dtype=np.uint8)

    # run through each pixel and draw the circle on our blank canvas
    for y in range(0,downsized_image_height):
        for x in range(0,downsized_image_width):
            cv2.circle(blank_image,(((x*multiplier)+padding),((y*multiplier)+padding)), int((0.6 * multiplier) * ((255-downsized_image[y][x])/255)), dots_colour, -1)

    # save our image
    cv2.imwrite(image_path_save, blank_image) #change image name
    return image_path_save

def merge(im1_path, im2_path, id, text):
    #im = Image.new("RGBA", (128, 128))
    # IMAGE_PATH = picture.image_filter(im2_path, id)
    COMPOSED_TSHIRT_ADD = "static/images/%s_composed.jpeg" %id
    im2 = Image.open(im2_path)
    im1 = Image.open(im1_path)

    im1 = im1.resize((768, 768))
    im2 = im2.resize((256, 384))

    im1.paste(im2, (256,192))
    draw = ImageDraw.Draw(im1)
    font = ImageFont.truetype("Rafigen.ttf", 34, encoding="unic")
    text_start_height = 600
    lines = textwrap.wrap(text, width=20)
    for line in lines:
        line_width, line_height = font.getsize(line)
        draw.text(((768 - line_width) / 2, text_start_height), 
                  line, font=font, fill=(12, 106, 106))
        text_start_height += line_height
    # draw.text((x, y),"Sample Text",(r,g,b))
    # draw.text((256, 600),text,(255,255,255),font=font)
    im1.save(COMPOSED_TSHIRT_ADD)
    return COMPOSED_TSHIRT_ADD

def merge_no_image(im1_path, id, text):
    #im = Image.new("RGBA", (128, 128))
    COMPOSED_TSHIRT_ADD = "static/images/%s_composed.jpeg" %id
    im1 = Image.open(im1_path)

    im1 = im1.resize((768, 768))

    draw = ImageDraw.Draw(im1)
    font = ImageFont.truetype("Rafigen.ttf", 34, encoding="unic")
    text_start_height = 300
    lines = textwrap.wrap(text, width=20)
    for line in lines:
        line_width, line_height = font.getsize(line)
        draw.text(((768 - line_width) / 2, text_start_height), 
                  line, font=font, fill=(12, 106, 106))
        text_start_height += line_height
    # draw.text((x, y),"Sample Text",(r,g,b))
    # draw.text((256,192),text,(255,255,255),font=font)
    im1.save(COMPOSED_TSHIRT_ADD)
    return COMPOSED_TSHIRT_ADD

def make_tshirt(id, combination=pd.DataFrame()):
    ANIMALS = ['Bird', 'Dog', 'Cat', 'Butterfly']
    PERSON = ['Celebrity', 'Rockstar', 'Cool people']
    ANIMALNPERSON = ['Butterfly and people', 'Human and animal']
    NONREALISTIC = ['Abstract', 'Aesthetic']

    BLACK_TSHIRT = "static/images/black.jpeg"
    WHITE_TSHIRT = "static/images/white.jpeg"
    COLOUR_TSHIRT = ["static/images/yellow.jpg",
                     "static/images/red.jpg",
                     "static/images/green.jpg",
                     "static/images/blue.jpg"]

    if combination['Animal'] == 1:
        retrieved_image = image_retrieve(random.choice(ANIMALS), id)
        if combination['Black'] == 1:
            completed_tshirt = merge(BLACK_TSHIRT, retrieved_image, id, combination['text'])
        elif combination['White'] == 1:
            completed_tshirt = merge(WHITE_TSHIRT, retrieved_image, id, combination['text'])
        elif combination['Colorful'] == 1:
            completed_tshirt = merge(random.choice(COLOUR_TSHIRT), retrieved_image, id, combination['text'])
        
    elif combination['Person'] == 1:
        retrieved_image = image_retrieve(random.choice(PERSON), id)
        if combination['Black'] == 1:
            completed_tshirt = merge(BLACK_TSHIRT, retrieved_image, id, combination['text'])
        elif combination['White'] == 1:
            completed_tshirt = merge(WHITE_TSHIRT, retrieved_image, id, combination['text'])
        elif combination['Colorful'] == 1:
            completed_tshirt = merge(random.choice(COLOUR_TSHIRT), retrieved_image, id, combination['text'])
    
    elif combination['AnimalnPerson'] == 1:
        retrieved_image = image_retrieve(random.choice(ANIMALNPERSON), id)
        if combination['Black'] == 1:
            completed_tshirt = merge(BLACK_TSHIRT, retrieved_image, id, combination['text'])
        elif combination['White'] == 1:
            completed_tshirt = merge(WHITE_TSHIRT, retrieved_image, id, combination['text'])
        elif combination['Colorful'] == 1:
            completed_tshirt = merge(random.choice(COLOUR_TSHIRT), retrieved_image, id, combination['text'])
    else:
        retrieved_image = image_retrieve(random.choice(NONREALISTIC), id)
        if combination['Black'] == 1:
            completed_tshirt = merge(BLACK_TSHIRT, retrieved_image, id, combination['text'])
        elif combination['White'] == 1:
            completed_tshirt = merge(WHITE_TSHIRT, retrieved_image, id, combination['text'])
        elif combination['Colorful'] == 1:
            completed_tshirt = merge(random.choice(COLOUR_TSHIRT),retrieved_image, id, combination['text'])
    return completed_tshirt
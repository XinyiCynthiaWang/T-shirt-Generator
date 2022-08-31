import io

from os import path
from google.cloud import vision
from google.cloud import language_v1


def detect_properties(path):
    """Detects image properties in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.image_properties(image=image)
    props = response.image_properties_annotation
    color_pixel_fraction = {}
    
    for color in props.dominant_colors.colors:
        color_pixel_fraction[color.pixel_fraction] = color.color
        
    if (color_pixel_fraction.keys()):
        return color_pixel_fraction[max(color_pixel_fraction.keys())]
    else:
        return None

def sentiment_analysis(text):
    try:
        if text == 'NaN' or text == 'None':
            return 0
        else:
            # Instantiates a client
            client = language_v1.LanguageServiceClient()

            # The text to analyze
            document = language_v1.Document(
                content=text, type_=language_v1.Document.Type.PLAIN_TEXT
            )

            # Detects the sentiment of the text
            sentiment = client.analyze_sentiment(
                request={"document": document}
            ).document_sentiment

            return sentiment.score
    except:
        return 0
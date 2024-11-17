import os
import json
import requests
from newspaper import Article
import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFont
import tweepy

# Global variables for title and summary
global title
global summary

# Configure API keys from environment variables
news_api_key = os.getenv("NEWS_API_KEY")
genai_api_key = os.getenv("GENAI_API_KEY")
api_key = os.getenv("TWITTER_CONSUMER_KEY")
api_secret = os.getenv("TWITTER_CONSUMER_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Initialize the Generative AI API
genai.configure(api_key=genai_api_key)

# File to store fetched article URLs
fetched_articles_file = "fetched_articles.json"

# Load previously fetched article URLs from the file
if os.path.exists(fetched_articles_file):
    with open(fetched_articles_file, "r") as file:
        try:
            fetched_urls = set(json.load(file))  # Safely load URLs
        except json.JSONDecodeError:
            fetched_urls = set()  # Handle file corruption or empty file
else:
    fetched_urls = set()

# Set up the News API endpoint and parameters
url = "https://newsapi.org/v2/top-headlines"
params = {
    'country': 'us',
    'category': 'technology',
    'apiKey': news_api_key
}

# Set up the Generative AI model configuration
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="tunedModels/newsx-xjuj5pke9bxg",
  generation_config=generation_config,
)

# Fetch the latest articles from News API
response = requests.get(url, params=params)
if response.status_code == 200:
    data = response.json()
    articles = data.get("articles", [])

    # Process the first unique technology article
    unique_article_found = False  # Flag to check if a unique article is found
    for article in articles:
        if article['url'] not in fetched_urls:  # Check if the article is already fetched
            fetched_urls.add(article['url'])  # Add it to the set of fetched URLs
            unique_article_found = True  # Mark as unique article found

            # Try to download and parse the article
            try:
                news_article = Article(article['url'])
                news_article.download()
                news_article.parse()

                # Pass full article text to the Generative AI model
                chat_session = model.start_chat(history=[])
                response = chat_session.send_message(news_article.text)

                # Display the response from the Generative AI model
                print(f"Title: {article['title']}")
                print(f"Full Text: {news_article.text}\n")
                print("AI Model Response:", response.text)
                title = article['title']
                summary = response.text
                # Stop after processing the first unique article
                break

            except Exception as e:
                print(f"Failed to retrieve full text for article: {article['title']}\nError: {e}")

    # Update the list of fetched articles only if a new article was found
    if unique_article_found:
        with open(fetched_articles_file, "w") as file:
            json.dump(list(fetched_urls), file)
    else:
        print("No new unique articles found.")
else:
    print("Failed to fetch articles. Status code:", response.status_code)

# Text and Image Handling (No changes here)
def draw_rounded_rectangle(width, height, corner_radius, fill_color, outline_color, outline_width):
    # Create a new image with transparent background
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Draw the rounded rectangle
    draw.rounded_rectangle([(0, 0), (width, height)], fill=fill_color, outline=outline_color, width=outline_width, radius=corner_radius)

    return image

def draw_original_rectangle(draw, width, height, corner_radius, fill_color, outline_color, outline_width):
    # Draw the sides of the original rectangle
    draw.rectangle([(corner_radius, 0), (width - corner_radius, height)], fill=fill_color, outline=outline_color, width=outline_width)
    draw.rectangle([(0, corner_radius), (width, height - corner_radius)], fill=fill_color, outline=outline_color, width=outline_width)

# Create the base image with rounded rectangle
def main():
    width, height = 860, 900
    corner_radius = 30
    fill_color = "#282828"
    outline_color = "grey"
    outline_width = 5

    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Draw the rounded rectangle and the original rectangle over it
    rounded_rectangle = draw_rounded_rectangle(width, height, corner_radius, fill_color, outline_color, outline_width)
    draw_original_rectangle(draw, width, height, corner_radius, fill_color, outline_color, outline_width)

    image = Image.alpha_composite(image, rounded_rectangle)

    # Save the base image
    image_rgb = image.convert("RGB")
    image_rgb.save("base.jpg", quality=95)

# Text generation function
def draw_text_on_image(image, text, font, max_width, max_height, x_offset, y_offset):
    draw = ImageDraw.Draw(image)
    lines = []
    words = text.split()
    current_line = ''
    for word in words:
        test_line = current_line + ' ' + word if current_line else word
        width, _ = draw.textsize(test_line, font=font)
        if width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)

    y = y_offset
    for line in lines:
        width, height = draw.textsize(line, font=font)
        draw.text((x_offset, y), line, font=font, fill=(255, 255, 255))
        y += height

# Load the base image and add text (title and summary)
if os.path.exists("base.jpg"):
    base_image = Image.open("base.jpg")
else:
    print("base.jpg not found, generating new image...")
    main()
    base_image = Image.open("base.jpg")

image_width, image_height = base_image.size

# Define font paths and sizes
title_font_path = "arialbold.ttf"  # Replace with correct path if necessary
summary_font_path = "arial.ttf"    # Replace with correct path if necessary
title_font_size = 50
summary_font_size = 46

# Create font objects
title_font = ImageFont.truetype(title_font_path, title_font_size)
summary_font = ImageFont.truetype(summary_font_path, summary_font_size)

# Define maximum width for text wrapping
max_text_width = image_width - 20
max_text_height = image_height - 60

# Calculate text positions
title_y_offset = 45
summary_y_offset = (ImageDraw.Draw(base_image).textsize(title, font=title_font)[1] + 60) * 2 + 15 + 25

# Add text to the image
draw_text_on_image(base_image, title, title_font, max_text_width, max_text_height, 15, title_y_offset)
draw_text_on_image(base_image, summary, summary_font, max_text_width, max_text_height, 15, summary_y_offset)

# Save the modified image
base_image.save("output.png")

# Twitter API setup (v1.1 and v2.0)
def get_twitter_conn_v1(api_key, api_secret, access_token, access_token_secret) -> tweepy.API:
    """Get twitter connection using v1.1"""
    auth = tweepy.OAuth1UserHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)

def get_twitter_conn_v2(api_key, api_secret, access_token, access_token_secret) -> tweepy.Client:
    """Get twitter connection using v2.0"""
    return tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

# Post to Twitter using v1.1 and v2.0
def post_to_twitter_v1_and_v2():
    # Initialize the Twitter clients
    client_v1 = get_twitter_conn_v1(api_key, api_secret, access_token, access_token_secret)
    client_v2 = get_twitter_conn_v2(api_key, api_secret, access_token, access_token_secret)
    
    # Upload media and post tweet using v1.1 API
    media_path = "output.png"
    media = client_v1.media_upload(filename=media_path)
    media_id = media.media_id
    
    # Post tweet using v2 API
    client_v2.create_tweet(text=title + " #Tech #Technology #News #ShortNews #AI #X #Xnews #Trending ", media_ids=[media_id])

post_to_twitter_v1_and_v2()

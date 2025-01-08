import json
import logging
import traceback

from openai import OpenAI, OpenAIError

# Logger configuration
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Loading configuration from JSON file
def load_config(config_file="config.json"):
    try:
        with open(config_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_file}")
        return {}
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON configuration file: {config_file}")
        return {}
    except Exception as e:
        logger.error(f"Unexpected error while loading config: {e}")
        logger.error(traceback.format_exc())
        return {}

# Loading API key
def load_api_key(file_path="API_KEY"):
    try:
        with open(file_path, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        logger.error(f"API_KEY file not found: {file_path}")
        return ""
    except Exception as e:
        logger.error(f"Error reading API_KEY file: {e}")
        logger.error(traceback.format_exc())
        return ""

# Reading article from file (supports large files)
def read_article(file_path):
    try:
        article_text = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                article_text.append(line.strip())
            article_text = " ".join(article_text)

        if not article_text.strip():
            logger.error(f"File is empty: {file_path}")
            return None
        return article_text

    except UnicodeDecodeError:
        logger.error(f"File encoding issue. Ensure the file is UTF-8 encoded: {file_path}")
        return None
    except Exception as e:
        logger.error(f"Error reading article: {e}")
        logger.error(traceback.format_exc())
        return None

# Generate HTML with OpenAI
def generate_html(article_text, openai_api_key, openai_model):
    try:
        if not openai_api_key:
            return ""
        client = OpenAI(api_key=openai_api_key)

        prompt = (
            "Convert the following article into HTML with proper structural division "
            "using <article> and <section> tags. "
            "1. HTML structure: Organize the content according to the hierarchy, using: "
            "<article> as the main frame for the entire article, "
            "<section> to logically divide the content into topical sections. "
            "2. Adding images: Identify appropriate places for images. "
            "Insert <img src=\"image_placeholder.jpg\"> tags in the selected locations. "
            "Assign a rich and detailed English prompt to the alt attribute, describing the image "
            "according to the following rules: "
            "Main Scene: Describe exactly what the focal point of the image is, e.g. technology, person, place. "
            "Action and Interaction: Include what is happening in the scene and what elements are interacting. "
            "Background Details: Add important information about the surroundings, e.g. landscape, technology, "
            "architectural details. Style and Aesthetics: Define the artistic style (e.g. realistic, futuristic) "
            "and dominant color scheme. Image Purpose: Make sure the description emphasizes the context and meaning "
            "of the image in relation to the article. "
            "Create descriptions in the form of complete, detailed sentences (min. 4-5 sentences). "
            "3. Image captions: Surround each image with a <figure> tag. "
            "Add a description of the image in the <figcaption> tag. "
            "4. Return code: Generate only HTML code containing content to be placed between <body> and </body>. "
            "Do not include <html>, <head>, or <body> tags. "
            "5. Code formatting rules: Keep it readable and indented. "
            "Each section must be logically described and properly tagged. "
            "Extract <footer> outside <article>. Keep number of paragraphs. "
            "Article body: "
            f"{article_text}"
        )

        completions = client.chat.completions.create(
            model=openai_model,
            messages=[{
                "role": "user",
                "content": prompt
            }],
        )

        return completions.choices[0].message.content
    except OpenAIError as e:
        logger.error(f"Open API error: {e}")
        logger.error(traceback.format_exc())
        return ""
    except Exception as e:
        logger.error(f"Unexpected error while generating HTML: {e}")
        logger.error(traceback.format_exc())
        return ""

# Text cleanup from Markdown HTML
def file_cleanup(text):
    # Removing Markdown blocks surrounded by ```html and ```
    cleaned_text = text.replace("```html", "").replace("```", "").strip()
    return cleaned_text

# Saving generated HTML to file
def save_html_to_file(content, output_file):
    try:
        with open(output_file, 'w', encoding='UTF-8') as file:
            file.write(content)
        logger.info(f"HTML content successfully saved to {output_file}.")
    except IOError as e:
        logger.error(f"IO error occurred while saving HTML to file {output_file}: {e}")
        logger.error(traceback.format_exc())
    except Exception as e:
        logger.error(f"Unexpected error occurred while saving HTML content to file {output_file}: {e}")
        logger.error(traceback.format_exc())

# Processing the article and generating HTML
def process_article(config):
    input_file = config.get("input_file", "article.txt")
    output_file = config.get("output_file", "artykul.html")
    api_key_file = config.get("api_key_file", "API_KEY")
    openai_model = config.get("openai_model", "gpt-4o-mini")

    try:
        openai_api_key = load_api_key(api_key_file)
        article_content = read_article(input_file)

        if article_content:
            html_content = generate_html(article_content, openai_api_key, openai_model)
            cleaned_content = file_cleanup(html_content)
            if cleaned_content:
                save_html_to_file(cleaned_content, output_file)
            else:
                logger.error("No HTML content generated.")
        else:
            logger.error("Article content is empty or not read properly.")
    except Exception as e:
        logger.error(f"Error in processing article: {e}")
        logger.error(traceback.format_exc())

# Starting the main function
if __name__ == "__main__":
    try:
        config = load_config()
        if config:
            process_article(config)
        else:
            logger.error("Failed to load configuration.")
    except Exception as e:
        logger.error(f"An error occurred in the main process: {e}")

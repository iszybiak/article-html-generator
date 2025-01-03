import json
import logging
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

# Loading API key
def load_api_key(file_path="API_KEY"):
    try:
        with open(file_path, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        logger.error(f"API_KEY file not found. {file_path}")
        return ""
    except Exception as e:
        logger.error(f"Error reading API_KEY file: {e}")
        return ""

# Reading article form file (supports large files)
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
        return None


# Generate HTML with OpenAI
def generate_html(article_text, openai_api_key, openai_model):
    try:
        if not openai_api_key:
            return ""
        client = OpenAI(api_key=openai_api_key)

        completions = client.chat.completions.create(
             model=openai_model,
             messages=[{
                 "role": "user",
                 "content": f"""Zredaguj poniższy artykuł, a natępie przekształć go do formatu HTML, strukturalnie podzieloneo z użyciem odpowiednich tagów HTML.
                            Zidentyfikuj miejsca, w których warto dodać obrazy, oznaczone tagiem <img src="image_placeholder.jpg">.
                            Do każdego utwórz dokładny prompt potrzebny do wygenerowania obrazu adekwatnego do atytkułu.
                            Treść prompte przypisz do atrybytu alt.
                            Umieść podpisy pod grafikami używając <figure> i <figcaption>.
                            Zwrócony kod powinien zawierać wyłącznie zawartość do wstawienia pomiędzy tagami <body> i </body>. 
                            Nie dołączaj znaczników <html>,<head> ani <body>.
                            Artykuł:
                            {article_text}"""
             }],
         )

        return completions.choices[0].message.content
    except OpenAIError as e:
        logger.error(f"Open API error: {e}")
        return ""

    except Exception as e:
        logger.error(f"Unexpected error while generating HTML: {e}")
        return ""


# Text cleanup form Markdown html
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
    except Exception as e:
        logger.error(f"Unexpected error occurred while saving HTML content to file {output_file}: {e}")

# Processing the article and generating HTML
def process_article(config):
    input_file = config.get("input_file", "article.txt")
    output_file = config.get("output_file", "artykul.html")
    api_key_file = config.get("api_key_file", "API_KEY")
    openai_model = config.get("openai_model", "model.json")

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



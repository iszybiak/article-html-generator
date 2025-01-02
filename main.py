from openai import OpenAI
from torch.distributed.elastic.agent.server.api import logger
import os
import re

def read_article(file_path):
    try:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return None
        with open(file_path, 'r', encoding='utf-8') as file:
            article_text = file.read().strip()

        if not article_text:
            logger.error(f"File is empty: {file_path}")
            return None

        return article_text

    except UnicodeDecodeError:
        logger.error(f"File encoding issue. Ensure the file is UTF-8 encoded: {file_path}")
        return None

    except Exception as e:
        logger.error(f"Error reading article : {e}")

def generate_html(article_text):
    try:
        try:
            with open("API_KEY", "r") as f:
                API_KEY = f.read().strip()
                if not API_KEY:
                    raise ValueError("API_KEY is empty. Please check the file.")
        except FileNotFoundError:
            logger.error("API_KEY file not found.")
            return ""
        except ValueError as e:
            logger.error(f"Error with API_KEY file: {e}")
            return ""
        except Exception as e:
            logger.error(f"Error reading API_KEY file: {e}")
            return ""
        client = OpenAI(api_key=API_KEY)


        completions = client.chat.completions.create(
             model="gpt-4o-mini",
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
    except Exception as e:
        logger.error(f"Unexpected error while generating HTML: {e}")
        return ""

#Oczyszczanie pliku ze składni Markdown
def file_cleanup(text):
    # Usuwanie bloków Markdown otoczonych przez ```html i ```
    cleaned_text = text.replace("```html", "").replace("```", "").strip()
    return cleaned_text


def save_html_to_file(content, output_file="artykul.html"):
    try:
        with open(output_file, 'w', encoding='UTF-8') as file:
            file.write(content)
        logger.info(f"HTML content successfully saved to {output_file}.")
    except IOError as e:
        logger.error(f"IO error occurred while saving HTML to file {output_file}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error occurred while saving HTML content to file {output_file}: {e}")


if __name__ == "__main__":
    try:
        article_content = read_article("article.txt")
        if article_content:
            html_content = generate_html(article_content)
            cleaned_content = file_cleanup(html_content)
            if cleaned_content:
                save_html_to_file(cleaned_content)
            else:
                logger.error("No HTML content generated.")
        else:
            logger.error("Article content is empty or not read properly.")
    except Exception as e:
        logger.error(f"An error occurred in the main process: {e}")



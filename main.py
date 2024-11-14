from openai import OpenAI
from torch.distributed.elastic.agent.server.api import logger


def read_article(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        article_text = file.read()
    return article_text

def generate_html(article_text):
    try:
        API_KEY= open("API_KEY", "r").read().strip()
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
        print(f"Error occurred while generating HTML: {e}")
        return ""

#Oczyszczanie pliku ze składni Markdown
def file_cleanup (text):
    lines = text.splitlines()
    if len(lines) > 2:
        lines = lines[1:-1]
    return '\n'.join(lines)

def save_html_to_file(content, output_file="artykul.html"):
    with open(output_file, 'w', encoding='UTF-8') as file:
        file.write(content)



if __name__ == "__main__":
    try:
        article_content = read_article("article.txt")
        html_content = file_cleanup(generate_html(article_content))
        save_html_to_file(html_content)
    except Exception as e:
        logger.error(f"An error occurred: {e}")



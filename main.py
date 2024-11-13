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
                            Każdy obrazek powinien mieć atrybut alt z dokładnym opisem promptu, który można użyć do wygenerowania grafiki.
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

def save_html_to_file(content, output_file="artykul.html"):
    with open(output_file, 'w', encoding='UTF-8') as file:
        file.write(content)


if __name__ == "__main__":
    try:
        article_content = read_article("article.txt")
        html_content = generate_html(article_content)
        save_html_to_file(html_content)
    except Exception as e:
        logger.error(f"An error occurred: {e}")



from openai import OpenAI

def read_article(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        article_text = file.read()
    return article_text

# API_KEY= open("API_KEY", "r").read().strip()
# client = OpenAI(api_key=API_KEY)
#
# completions = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[{
#         "role": "user",
#         "content": "Say this is a test",
#     }],
# )
#
# print(completions.choices[0].message.content)

from openai import OpenAI


API_KEY= open("API_KEY", "r").read().strip()
client = OpenAI(api_key=API_KEY)

completions = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{
        "role": "user",
        "content": "Say this is a test",
    }],
)

print(completions.choices[0].message.content)

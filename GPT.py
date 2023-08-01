import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_completion(role, content, model="gpt-3.5-turbo"):
    res = openai.ChatCompletion.create(model=model, messages=[{"role": "system", "content": role}, {"role": "user", "content": content}])
    return res.choices[0]["message"]["content"]

import json
import os
from openai import OpenAI
from pydantic import BaseModel
from tqdm import tqdm
import re
from dotenv import load_dotenv

load_dotenv()

books = {
    1: "Harry Potter and the Philosopher's Stone",
    2: "Harry Potter and the Chamber of Secrets",
    3: "Harry Potter and the Prisoner of Azkaban",
    4: "Harry Potter and the Goblet of Fire",
    5: "Harry Potter and the Order of the Phoenix",
    6: "Harry Potter and the Half-Blood Prince",
    7: "Harry Potter and the Deathly Hallows",
}


def get_chapters(book):
    chapters = []
    with open(f"./data/books/{book}.txt") as f:
        text = f.read()
        chapters = re.split(
            r'chapter \d+[\r\n]+(.*[^\r\n])', text, flags=re.IGNORECASE)[1:]
        if len(chapters) == 0 or len(chapters) % 2 != 0:
            raise Exception(f"Failed to parse chapters for {book}")
    return [(chapters[2*i].strip(), chapters[2*i+1].strip()) for i in range(len(chapters) // 2)]


def get_chunks(book, chunk_size=50):
    chunks = []
    with open(f"./data/{book}.txt") as f:
        chapters = get_chapters(book)
        for chapter in chapters:
            chunks.extend(['\n'.join(chapter.split('\n')[i:i+chunk_size])
                          for i in range(0, len(chapter), chunk_size)])
    return chunks


class Quote(BaseModel):
    speaker: str
    content: str


class Quotes(BaseModel):
    quotes: list[Quote]


def get_quote(text, client, model):
    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": "You are an editor who can detects and extracts quotes and their speaker from text."},
            {"role": "user", "content": text},
        ],
        response_format=Quotes
    )
    return completion


def get_quotes_for_book(book, client, model="gpt-4o"):
    quotes = []
    chapters = get_chapters(book)
    for title, chapter in tqdm(chapters):
        response = get_quote(chapter, client, model)
        q_model = response.choices[0].message.parsed
        for q in q_model.dict()['quotes']:
            quotes.append({"book": books[book], "chapter": title, **q})
    return quotes


client = OpenAI(base_url="https://api.openai.com/v1",
                api_key=os.getenv("OPENAI_API_KEY"))

for book in range(1, 8):
    quotes = get_quotes_for_book(book, client)
    with open(f"./data/quotes/{book}.json", "w") as f:
        f.write(json.dumps(quotes, indent=4))

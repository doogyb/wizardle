# %%
import pandas as pd
from os import walk

# %%
paths = []
for (dirpath, dirnames, filenames) in walk('data/quotes'):
    paths.extend(filenames)

books = [pd.read_json(f'data/quotes/{path}') for path in paths]
df = pd.concat(books, ignore_index=True)

# %%
mappings = pd.read_csv('./data/characters/mappings.csv')
mappings = mappings.to_dict(orient='records')
mappings = {row['speaker']: row['name'] for row in mappings}

# %%
df['speaker'] = df['speaker'].apply(
    lambda x: mappings[x] if x in mappings else x)
df = df[df['content'].str.len() > 30]
df.to_json('./data/quotes/filtered.json')

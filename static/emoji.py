import os
import pickle
import cohere
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity

# KEY_NAME = 'COHERE_API_KEY'
KEY_NAME = 'COHERE_API_PROD_KEY'

if KEY_NAME not in os.environ:
    raise Exception
co = cohere.Client(os.environ[KEY_NAME])


# def cosine_similarity(a: np.array, b: np.array) -> float:
# np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def embed_strings(strings: list[str]):
    return np.array(co.embed(strings).embeddings)


def store_embeddings(filename: str = 'static/all_emojis.csv'):
    import pandas as pd
    df = pd.read_csv(filename)
    names, emojis = df['Name'], df['Representation']
    # print(list(names))
    embeddings = embed_strings(list(names))
    assert embeddings.shape[0] == len(emojis)
    with open('embeddings.npy', 'wb') as f:
        np.save(f, embeddings)
    with open('all_emojis.pickle', 'wb') as f:
        pickle.dump(emojis.to_dict(), f)


def load_embeddings() -> tuple[np.array, dict[int, str]]:
    with open('embeddings.npy', 'rb') as f:
        embeddings = np.load(f)
    with open('all_emojis.pickle', 'rb') as f:
        emoji_dict = pickle.load(f)
    return embeddings, emoji_dict


def top_idx(input: str, embeddings: np.array) -> int:
    input_embed = np.array(co.embed([input]).embeddings)
    similarities = cosine_similarity(input_embed, embeddings)
    print(similarities.shape)
    print('max', np.max(similarities), 'argmax', np.argmax(similarities))
    print('min', np.min(similarities))
    return np.argmax(similarities)


if __name__ == '__main__':
    store_embeddings()
    embeddings, emoji_dict = load_embeddings()
    input_string = ''
    while input_string != 'quit':
        input_string = input(
            "Please enter a description for an emoji, or enter 'quit': ")
        top_emoji = emoji_dict[top_idx(input_string, embeddings)]
        print(top_emoji)

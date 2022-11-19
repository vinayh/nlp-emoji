import os
import pickle
import cohere
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances

# KEY_NAME = 'COHERE_API_KEY'
KEY_NAME = 'COHERE_API_PROD_KEY'

if KEY_NAME not in os.environ:
    raise Exception
co = cohere.Client(os.environ[KEY_NAME])


def embed_strings(strings: list[str]):
    return np.array(co.embed(strings).embeddings)


def store_embeddings(emoji_csv: str = 'static/all_emojis.csv', embed_names=False):
    import pandas as pd
    df = pd.read_csv(emoji_csv)
    names, emojis = df['Name'], df['Representation']
    if embed_names:
        print(list(names))
        embeddings = embed_strings(list(names))
        assert embeddings.shape[0] == len(emojis)
        with open('static/embeddings.npy', 'wb') as f:
            np.save(f, embeddings)
    emoji_dict = dict(zip(range(len(names)), zip(names, emojis)))
    with open('static/all_emojis.pickle', 'wb') as f:
        pickle.dump(emoji_dict, f)


def load_embeddings() -> tuple[np.array, dict[int, str]]:
    with open('static/embeddings.npy', 'rb') as f:
        embeddings = np.load(f)
    with open('static/all_emojis.pickle', 'rb') as f:
        emoji_dict = pickle.load(f)
    return embeddings, emoji_dict


def top_idx(input: str, embeddings: np.array, k: int = 1) -> int:
    input_embed = np.array(co.embed([input]).embeddings)
    similarities = cosine_similarity(input_embed, embeddings).flatten()
    if k == 1:
        return [np.argmax(similarities)]
    else:
        ind = np.argpartition(similarities, -k)[-k:]
        return ind[np.argsort(-similarities[ind])]
    # return np.argmin(similarities)


if __name__ == '__main__':
    store_embeddings(embed_names=False)
    embeddings, emoji_dict = load_embeddings()
    input_string = ''
    while input_string != 'quit':
        input_string = input(
            "Please enter a description for an emoji, or enter 'quit': ")
        top_emoji = [emoji_dict[i]
                     for i in top_idx(input_string, embeddings, k=3)]
        print(top_emoji)

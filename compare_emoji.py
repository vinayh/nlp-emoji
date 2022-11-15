from emoji import load_embeddings, top_idx

if __name__ == '__main__':
    # store_embeddings()
    embeddings, emoji_dict = load_embeddings()
    input_string = ''
    while input_string != 'quit':
        input_string = input(
            "Please enter a description for an emoji, or enter 'quit': ")
        top_emoji = emoji_dict[top_idx(input_string, embeddings)]
        print(top_emoji)

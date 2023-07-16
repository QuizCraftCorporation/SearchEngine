from langchain.embeddings import HuggingFaceEmbeddings

class TextBase():
    def __init__(self) -> None:
        self.embeddings = HuggingFaceEmbeddings(cache_folder="models/all-mpnet-base-v2")

    def search():
        pass

    def add_new():
        pass

    def delete():
        pass

    def clear():
        pass


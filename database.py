import os
import pathlib
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document

SAVE_FOLDER = os.path.join(pathlib.Path(__file__).parent.resolve(), "./vector_store")

class TextDataBase():
    def __init__(self) -> None:
        self.embeddings = HuggingFaceEmbeddings(model_name="./models/all-mpnet-base-v2")
        self.db = None
        if os.path.exists(os.path.join(SAVE_FOLDER, "index.faiss")):
            self.db = FAISS.load_local(SAVE_FOLDER, embeddings=self.embeddings)

    def search(self, query: str, number_of_results: int) -> tuple:
        if self.db == None:
            return ("empty", [])

        docs = self.db.similarity_search(query, k=number_of_results)
        the_most_similar_quizzes = []
        for doc in docs:
            quiz = doc.page_content
            the_most_similar_quizzes.append((quiz, doc.metadata["unique_name"]))
        
        return ("ok", the_most_similar_quizzes)

    def add_text(self, text: str, unique_name: str) -> None:
        document = Document(page_content=text, metadata=dict(unique_name=unique_name))

        if self.db == None:
            self.db = FAISS.from_documents([document], embedding=self.embeddings)
        else:
            self.db.add_documents([document])
        self.db.save_local(SAVE_FOLDER)
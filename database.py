import os
import pathlib
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document

cur_file_path = pathlib.Path(__file__).parent.resolve()
SAVE_FOLDER = os.path.join(cur_file_path, "vector_store")

class TextDataBase():
    """
    Text database based on FAISS with all-mpnet-base-v2 model for embeddings.
    """
    
    def __init__(self) -> None:
        """
        Load database.
        """
        
        self.embeddings = HuggingFaceEmbeddings(model_name=os.path.join(cur_file_path, "models/all-mpnet-base-v2"))
        self.db = None
        if os.path.exists(os.path.join(SAVE_FOLDER, "index.faiss")):
            self.db = FAISS.load_local(SAVE_FOLDER, embeddings=self.embeddings)

    def search(self, query: str, number_of_results: int) -> tuple:
        """
        Perform search operation.

        Args:
            query (str): Search query.
            number_of_results(int): How much found texts must be returned.

        Returns:
            tuple[str, list[tuple[str, str]]]: Tuple with exit code and list of texts sorted according to similarity to query.
            Each text returned with it own identifier inside tuple.
        """
        if self.db == None:
            return ("empty", [])

        docs = self.db.similarity_search(query, k=number_of_results)
        the_most_similar_quizzes = []
        for doc in docs:
            quiz = doc.page_content
            the_most_similar_quizzes.append((quiz, doc.metadata["unique_name"]))
        
        return ("ok", the_most_similar_quizzes)

    def add_text(self, text: str, unique_name: str) -> None:
        """
        Add new text in a vector database.

        Args:
            text (str): Text to save.
            unique_name(str): Unique text identifier.
        """
        
        document = Document(page_content=text, metadata=dict(unique_name=unique_name))

        if self.db == None:
            self.db = FAISS.from_documents([document], embedding=self.embeddings)
        else:
            self.db.add_documents([document])
        self.db.save_local(SAVE_FOLDER)

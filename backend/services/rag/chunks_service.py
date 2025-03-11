from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document as LangchainDocument

class ChunksService:      
    def chunk(self, documents: List[LangchainDocument], 
              chunk_size: int = 1000, 
              percentage_overlap: float = 0.15) -> List[LangchainDocument]:
        text_splitter = RecursiveCharacterTextSplitter(
            separators=[
                "\n## ", "\n### ", "\n#### ", "\n##### ", "\n###### ",
                "\n\n", 
                "\n- ", "\n* ", "\n+ ", "\n1. ", "\n2. ", "\n3. ",
                "\n", 
                ". ", "! ", "? ",
                " ", 
                ""
            ],
            chunk_size=chunk_size,
            chunk_overlap=percentage_overlap * chunk_size
        )
        return text_splitter.split_documents(documents)
    
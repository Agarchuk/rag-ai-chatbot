from typing import Any, Dict, List
import chromadb
import os
from chromadb.utils import embedding_functions
from dtos.chunk_data import ChunkData
from dtos.relevant_context_dto import RelevantContextDto
from langchain_core.documents import Document as LangchainDocument
from utils.logger import log_error, log_info
import streamlit as st

class CollectionsService:
    def __init__(self, persist_directory: str = "./chroma_db", default_model: str = "all-MiniLM-L6-v2"):
        os.makedirs(persist_directory, exist_ok=True)
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.default_model = default_model
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(self.default_model)

    def get_collection(self, collection_name: str):
        return self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function
        )
    
    def get_collection_chunks(self, collection_name: str):
        return self.get_collection(collection_name).get()

    def get_chunks_by_ids(self, collection_name: str, chunk_ids: List[str]) -> List[LangchainDocument]:
        collection = self.get_collection(collection_name)
        return collection.get(ids=chunk_ids)
    
    def add_collection_chunk(self, collection_name: str, chunk_id: str, chunk_text: str, 
                           metadata: Dict[str, Any]):
        collection = self.get_collection(collection_name)
        collection.add(
            documents=[chunk_text],
            metadatas=[metadata],
            ids=[chunk_id]
        )
        return chunk_id
    
    def get_relevant_context(self, chunk_ids_and_collection_name_by_document_id: dict[int, dict[str, list[int]]], 
                           query_text: str, 
                           max_length: int = 4000) -> RelevantContextDto:
        
        try:
            chunk_data = []
            context = ""
            
            for document_id, chunk_ids_and_collection_name in chunk_ids_and_collection_name_by_document_id.items():
                collection_name = chunk_ids_and_collection_name["collection_name"]
                chunk_ids = chunk_ids_and_collection_name["chunk_ids"]
                log_info(f"Querying collection with chunk_ids: {chunk_ids}, query_text: {query_text}, collection_name: {collection_name}")
                results = self._query_collection(collection_name, query_text, 
                                               chunk_ids=chunk_ids)
                
                
                for i, doc in enumerate(results["documents"][0]):
                    metadata = results["metadatas"][0][i] if results["metadatas"][0] else {}
                    chunk_data.append(ChunkData(
                        text=doc,
                        document_name=metadata.get("document_name", ""),
                        id=results["ids"][0][i],
                        distance=results["distances"][0][i],
                        document_id=document_id
                    ))
                    
                    if len(context) + len(doc) + 100 < max_length:
                        context += doc + "\n\n"

            return RelevantContextDto(
                context=context, 
                chunk_data=chunk_data
            )
        except Exception as e:
            log_error("Error getting relevant context", str(e))
            return RelevantContextDto(context="", chunk_data=[]) 

    
    def delete_collection(self, collection_name: str):
        self.client.delete_collection(name=collection_name)

    def _query_collection(self, collection_name: str, query_text: str, 
                        n_results: int = 4, chunk_ids: List[int] = None) -> dict:
        collection = self.get_collection(collection_name)
        where_filter = {"chunk_id": {"$in": chunk_ids}} if chunk_ids else None
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=where_filter
        )
        log_info(f"Query results: {results}")
        return results

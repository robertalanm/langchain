from typing import Dict, Type


"""Wrappers on top of vector stores."""
from langchain.vectorstores.atlas import AtlasDB
from langchain.vectorstores.base import VectorStore
from langchain.vectorstores.chroma import Chroma
from langchain.vectorstores.deeplake import DeepLake
from langchain.vectorstores.elastic_vector_search import ElasticVectorSearch
from langchain.vectorstores.faiss import FAISS
from langchain.vectorstores.milvus import Milvus
from langchain.vectorstores.opensearch_vector_search import OpenSearchVectorSearch
from langchain.vectorstores.pinecone import Pinecone
from langchain.vectorstores.qdrant import Qdrant
from langchain.vectorstores.weaviate import Weaviate

__all__ = [
    "ElasticVectorSearch",
    "FAISS",
    "VectorStore",
    "Pinecone",
    "Weaviate",
    "Qdrant",
    "Milvus",
    "Chroma",
    "OpenSearchVectorSearch",
    "AtlasDB",
    "DeepLake",
]

type_to_cls_dict: Dict[str, Type[VectorStore]] = {
    "elastic_vector_search": ElasticVectorSearch,
    "faiss": FAISS,
    "pinecone": Pinecone,
    "weaviate": Weaviate,
    "qdrant": Qdrant,
    "milvus": Milvus,
    "chroma": Chroma,
    "opensearch_vector_search": OpenSearchVectorSearch,
    "atlas_db": AtlasDB,
    "deep_lake": DeepLake,
}


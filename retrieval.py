from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from embeddings import generate_email_embeddings
from typing import Dict, List, Tuple, Optional
from embeddings import DataEmbedder
import faiss
import threading
from concurrent.futures import ThreadPoolExecutor

class SemanticRetriever:
    def __init__(self, dimension: int = 1536, index_type: str = 'l2'):
        """
        Initialize the retriever
        
        Args:
            dimension: Dimension of embeddings (1536 for text-embedding-ada-002)
            index_type: Type of FAISS index ('l2' or 'cosine')
        """
        self.dimension = dimension
        self.embedder = DataEmbedder()
        self.index_type = index_type
        self.index = None
        self.id_map = {}  # Maps FAISS ids to original data ids
        self._index_lock = threading.Lock()
        
    def _init_index(self):
        """Initialize FAISS index based on type"""
        if self.index_type == 'cosine':
            self.index = faiss.IndexFlatIP(self.dimension)  # Inner product for cosine similarity
        else:
            self.index = faiss.IndexFlatL2(self.dimension)  # L2 distance
            
    def add_items(self, items: List[dict], batch_size: int = 1000) -> None:
        """
        Add items to the index
        
        Args:
            items: List of items to index
            batch_size: Number of items to process at once
        """
        with self._index_lock:
            if self.index is None:
                self._init_index()
            
            # Generate embeddings in batches
            embeddings = self.embedder.batch_embed(items)
            
            # Convert embeddings to numpy array and normalize if using cosine similarity
            vectors = []
            for idx, emb in embeddings.items():
                if emb is not None:
                    self.id_map[len(vectors)] = idx
                    vectors.append(emb)
            
            vectors = np.array(vectors).astype('float32')
            if self.index_type == 'cosine':
                faiss.normalize_L2(vectors)
            
            # Add to index in batches
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i + batch_size]
                self.index.add(batch)
    
    def search(self, query: str, k: int = 10, threshold: float = None) -> List[Tuple[int, float]]:
        """
        Search for similar items
        
        Args:
            query: Search query
            k: Number of results to return
            threshold: Optional similarity threshold
            
        Returns:
            List of (item_id, similarity_score) tuples
        """
        with self._index_lock:
            if self.index is None or self.index.ntotal == 0:
                return []
            
            # Generate query embedding
            query_embedding = self.embedder.embed_single(query)
            if query_embedding is None:
                return []
            
            # Reshape and convert type
            query_vector = np.array([query_embedding]).astype('float32')
            if self.index_type == 'cosine':
                faiss.normalize_L2(query_vector)
            
            # Search
            distances, indices = self.index.search(query_vector, k)
            
            # Convert FAISS ids to original ids and apply threshold
            results = []
            for dist, idx in zip(distances[0], indices[0]):
                if idx != -1:  # Valid index
                    score = 1 - dist/2 if self.index_type == 'l2' else dist
                    if threshold is None or score >= threshold:
                        original_id = self.id_map.get(idx, idx)
                        results.append((original_id, float(score)))
            
            return results
    
    def batch_search(self, queries: List[str], k: int = 10, 
                    threshold: float = None, max_workers: int = 4) -> List[List[Tuple[int, float]]]:
        """
        Search for multiple queries in parallel
        
        Args:
            queries: List of search queries
            k: Number of results per query
            threshold: Optional similarity threshold
            max_workers: Maximum number of parallel workers
            
        Returns:
            List of results for each query
        """
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(
                lambda q: self.search(q, k, threshold),
                queries
            ))
        return results
    
    def update_item(self, item_id: int, new_item: dict) -> bool:
        """
        Update an existing item
        
        Args:
            item_id: ID of item to update
            new_item: New item data
            
        Returns:
            True if update successful
        """
        # Find the FAISS id
        faiss_id = None
        for fid, oid in self.id_map.items():
            if oid == item_id:
                faiss_id = fid
                break
        
        if faiss_id is None:
            return False
            
        # Generate new embedding
        new_embedding = self.embedder.embed_single(new_item)
        if new_embedding is None:
            return False
            
        # Update the index
        with self._index_lock:
            vector = np.array([new_embedding]).astype('float32')
            if self.index_type == 'cosine':
                faiss.normalize_L2(vector)
            self.index.remove_ids(np.array([faiss_id]))
            self.index.add(vector)
            
        return True

# For backward compatibility
def retrieve_emails(query: str, email_embeddings: Dict[int, np.ndarray], 
                   k: int = 10) -> List[Tuple[int, float]]:
    """Legacy function for backward compatibility"""
    retriever = SemanticRetriever()
    
    # Convert email_embeddings to list format
    items = [{'id': idx, 'embedding': emb} for idx, emb in email_embeddings.items()]
    retriever.add_items(items)
    
    return retriever.search(query, k)

def retrieve_emails(query, email_embeddings, top_k=3):
    """
    Retrieve top-k most relevant emails for the given query.
    
    Args:
        query: Query string
        email_embeddings: Dictionary mapping thread_id to numpy array of embeddings
        top_k: Number of results to return
    
    Returns:
        List of thread_ids sorted by relevance
    """
    retriever = SemanticRetriever()
    
    # Convert email_embeddings to list format
    items = [{'id': idx, 'embedding': emb} for idx, emb in email_embeddings.items()]
    retriever.add_items(items)
    
    results = retriever.search(query, top_k)
    return [item[0] for item in results]

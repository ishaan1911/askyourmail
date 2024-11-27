import numpy as np
import pickle
import os
from typing import Dict, List, Optional
from embeddings import DataEmbedder
from retrieval import SemanticRetriever

class EmailStore:
    def __init__(self, storage_path: str = "email_embeddings.pkl"):
        """
        Initialize the email store
        
        Args:
            storage_path: Path to store the embeddings
        """
        self.storage_path = storage_path
        self.embedder = DataEmbedder()
        self.retriever = SemanticRetriever()
        self.email_embeddings: Dict[int, np.ndarray] = {}
        self.load_embeddings()
    
    def load_embeddings(self) -> None:
        """Load existing embeddings from disk if they exist"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'rb') as f:
                    self.email_embeddings = pickle.load(f)
                # Initialize retriever with loaded embeddings
                self.retriever.add_items([
                    {'id': id, 'embedding': emb} 
                    for id, emb in self.email_embeddings.items()
                ])
            except Exception as e:
                print(f"Error loading embeddings: {e}")
    
    def save_embeddings(self) -> None:
        """Save embeddings to disk"""
        try:
            with open(self.storage_path, 'wb') as f:
                pickle.dump(self.email_embeddings, f)
        except Exception as e:
            print(f"Error saving embeddings: {e}")
    
    def create_embeddings(self, emails: List[dict]) -> None:
        """
        Create embeddings for new emails
        
        Args:
            emails: List of email dictionaries
        """
        # Generate embeddings
        new_embeddings = self.embedder.batch_embed(emails)
        
        # Update storage
        for idx, embedding in new_embeddings.items():
            if embedding is not None:
                self.email_embeddings[idx] = embedding
        
        # Update retriever
        self.retriever.add_items([
            {'id': id, 'embedding': emb} 
            for id, emb in new_embeddings.items()
        ])
        
        # Save to disk
        self.save_embeddings()
    
    def update_embeddings(self, emails: List[dict]) -> None:
        """
        Update embeddings for existing emails or add new ones
        
        Args:
            emails: List of email dictionaries
        """
        # Only process emails that don't have embeddings or need updates
        emails_to_update = [
            email for email in emails
            if email['id'] not in self.email_embeddings
        ]
        
        if emails_to_update:
            self.create_embeddings(emails_to_update)
    
    def search(self, query: str, k: int = 10) -> List[tuple]:
        """
        Search emails using the query
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of (email_id, score) tuples
        """
        return self.retriever.search(query, k)

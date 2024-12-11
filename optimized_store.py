import numpy as np
import sqlite3
import os
from typing import Dict, List, Optional, Iterator
from embeddings import DataEmbedder
from retrieval import SemanticRetriever
from datetime import datetime
import faiss
from queue import Queue
from threading import Thread, Lock
import time

class OptimizedEmailStore:
    def __init__(self, db_path: str = "email_store.db", 
                 index_path: str = "faiss_index",
                 batch_size: int = 100,
                 processing_interval: int = 300):  # 5 minutes
        """
        Initialize optimized email store
        
        Args:
            db_path: Path to SQLite database
            index_path: Directory to store FAISS index
            batch_size: Number of emails to process at once
            processing_interval: Seconds between processing batches
        """
        self.db_path = db_path
        self.index_path = index_path
        self.batch_size = batch_size
        self.processing_interval = processing_interval
        
        self.embedder = DataEmbedder()
        self.retriever = SemanticRetriever()
        self.processing_queue = Queue()
        self.lock = Lock()
        
        self._init_database()
        self._init_index()
        self._start_background_processor()
    
    def _init_database(self):
        """Initialize SQLite database with necessary tables"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS embeddings (
                    email_id INTEGER PRIMARY KEY,
                    embedding BLOB,
                    created_at TIMESTAMP,
                    processed BOOLEAN DEFAULT FALSE
                )
            ''')
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_processed 
                ON embeddings(processed)
            ''')
    
    def _init_index(self):
        """Initialize or load FAISS index"""
        if os.path.exists(f"{self.index_path}.index"):
            self.retriever.index = faiss.read_index(f"{self.index_path}.index")
            # Load ID mapping
            with open(f"{self.index_path}.map", 'rb') as f:
                self.retriever.id_map = np.load(f)
        else:
            os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
    
    def _save_index(self):
        """Save FAISS index to disk"""
        with self.lock:
            faiss.write_index(self.retriever.index, f"{self.index_path}.index")
            with open(f"{self.index_path}.map", 'wb') as f:
                np.save(f, self.retriever.id_map)
    
    def _start_background_processor(self):
        """Start background thread for processing email queue"""
        def process_queue():
            while True:
                batch = []
                while len(batch) < self.batch_size:
                    try:
                        email = self.processing_queue.get_nowait()
                        batch.append(email)
                    except Queue.Empty:
                        break
                
                if batch:
                    self._process_batch(batch)
                
                time.sleep(self.processing_interval)
        
        thread = Thread(target=process_queue, daemon=True)
        thread.start()
    
    def _process_batch(self, emails: List[dict]):
        """Process a batch of emails"""
        # Generate embeddings
        embeddings = self.embedder.batch_embed(emails)
        
        # Store in database
        with sqlite3.connect(self.db_path) as conn:
            for idx, embedding in embeddings.items():
                if embedding is not None:
                    conn.execute(
                        'INSERT OR REPLACE INTO embeddings (email_id, embedding, created_at, processed) '
                        'VALUES (?, ?, ?, ?)',
                        (idx, embedding.tobytes(), datetime.now(), True)
                    )
        
        # Update FAISS index
        with self.lock:
            self.retriever.add_items([
                {'id': id, 'embedding': emb} 
                for id, emb in embeddings.items()
            ])
        
        # Periodically save index
        self._save_index()
    
    def queue_emails(self, emails: List[dict]):
        """
        Queue emails for processing
        
        Args:
            emails: List of email dictionaries
        """
        for email in emails:
            self.processing_queue.put(email)
    
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
    
    def get_queue_size(self) -> int:
        """Get number of emails waiting to be processed"""
        return self.processing_queue.qsize()
    
    def get_processing_stats(self) -> Dict:
        """Get processing statistics"""
        with sqlite3.connect(self.db_path) as conn:
            total = conn.execute('SELECT COUNT(*) FROM embeddings').fetchone()[0]
            processed = conn.execute(
                'SELECT COUNT(*) FROM embeddings WHERE processed = 1'
            ).fetchone()[0]
            
        return {
            'total_emails': total,
            'processed_emails': processed,
            'queue_size': self.get_queue_size()
        }

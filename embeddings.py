import openai
import os
import numpy as np
from typing import Union, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv('key.env')
openai.api_key = os.getenv('OPENAI_API_KEY')

class DataEmbedder:
    def __init__(self, content_field: str = 'content', batch_size: int = 100):
        """
        Initialize the embedder
        
        Args:
            content_field: Field name containing the text to embed
            batch_size: Number of items to embed in one batch
        """
        self.content_field = content_field
        self.batch_size = batch_size
        
    def extract_text(self, data: Union[str, Dict[str, Any]]) -> Optional[str]:
        """
        Extract text to embed from various data types
        
        Args:
            data: Input data (string or dictionary)
            
        Returns:
            Text to embed or None if no valid text found
        """
        try:
            if isinstance(data, str):
                return data
            elif isinstance(data, dict):
                # Try to get text from specified field
                if self.content_field in data:
                    return str(data[self.content_field])
                
                # Fallback: concatenate all string/number values
                text_parts = []
                for key, value in data.items():
                    if isinstance(value, (str, int, float)):
                        text_parts.append(f"{key}: {value}")
                return " ".join(text_parts)
            else:
                # For other types, convert to string
                return str(data)
        except Exception as e:
            print(f"Error extracting text: {str(e)}")
            return None

    def generate_embedding(self, text: str) -> Optional[np.ndarray]:
        """
        Generate embedding for a single text
        
        Args:
            text: Text to embed
            
        Returns:
            Numpy array of embeddings or None if failed
        """
        try:
            if not text.strip():
                return None
                
            response = openai.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            return np.array(response.data[0].embedding)
            
        except Exception as e:
            print(f"Error generating embedding: {str(e)}")
            return None

    def batch_embed(self, data_list: list) -> Dict[int, np.ndarray]:
        """
        Generate embeddings for a list of data items in batches
        
        Args:
            data_list: List of items to embed
            
        Returns:
            Dictionary mapping indices to embeddings
        """
        embeddings = {}
        
        for i in range(0, len(data_list), self.batch_size):
            batch = data_list[i:i + self.batch_size]
            print(f"Processing batch {i//self.batch_size + 1}/{(len(data_list)-1)//self.batch_size + 1}")
            
            for j, item in enumerate(batch):
                idx = i + j
                
                # Extract text
                text = self.extract_text(item)
                if text is None:
                    continue
                
                # Generate embedding
                embedding = self.generate_embedding(text)
                if embedding is not None:
                    embeddings[idx] = embedding
        
        return embeddings

    def embed_single(self, data: Union[str, Dict[str, Any]]) -> Optional[np.ndarray]:
        """
        Generate embedding for a single data item
        
        Args:
            data: Item to embed
            
        Returns:
            Numpy array of embeddings or None if failed
        """
        text = self.extract_text(data)
        if text is None:
            return None
        
        return self.generate_embedding(text)

# For backward compatibility
def generate_email_embeddings(input_data):
    """Legacy function for backward compatibility"""
    embedder = DataEmbedder()
    if isinstance(input_data, list):
        return embedder.batch_embed(input_data)
    else:
        return embedder.embed_single(input_data)

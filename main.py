import json
from datetime import datetime
from dateutil import parser
from colorama import init, Fore, Style
from retrieval import SemanticRetriever
import re

# Initialize colorama for colored output
init()

class EmailSearchSystem:
    def __init__(self, data_file="dataset1.json"):
        """Initialize the email search system"""
        # Load emails
        with open(data_file, "r") as file:
            self.emails = json.load(file)
            
        # Initialize retriever
        self.retriever = SemanticRetriever(content_field="content")
        self.retriever.add_items(self.emails)
        
        # Create email index by various fields
        self._create_indices()

    def _create_indices(self):
        """Create indices for quick searching"""
        self.sender_index = {}
        self.recipient_index = {}
        self.date_index = {}
        
        for idx, email in enumerate(self.emails):
            # Index sender
            sender = email.get('from', '').lower()
            self.sender_index.setdefault(sender, []).append(idx)
            
            # Index recipients
            for recipient in email.get('to', []):
                recipient = recipient.lower()
                self.recipient_index.setdefault(recipient, []).append(idx)
            
            # Index date (by year, month, day)
            try:
                date = datetime.fromtimestamp(email['timestamp'] / 1000)
                date_key = date.strftime('%Y-%m-%d')
                self.date_index.setdefault(date_key, []).append(idx)
            except (KeyError, ValueError):
                pass

    def _format_email(self, email, highlight_terms=None):
        """Format email for display with optional term highlighting"""
        # Format basic info
        formatted = f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n"
        formatted += f"{Fore.GREEN}From:{Style.RESET_ALL} {email.get('from', 'Unknown')}\n"
        formatted += f"{Fore.GREEN}To:{Style.RESET_ALL} {', '.join(email.get('to', ['Unknown']))}\n"
        formatted += f"{Fore.GREEN}Subject:{Style.RESET_ALL} {email.get('subject', 'No Subject')}\n"
        
        # Format date
        timestamp = email.get('timestamp', 0) / 1000
        date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        formatted += f"{Fore.GREEN}Date:{Style.RESET_ALL} {date_str}\n"
        
        # Format content with highlighting
        content = email.get('content', '')
        if highlight_terms and content:
            for term in highlight_terms:
                pattern = re.compile(re.escape(term), re.IGNORECASE)
                content = pattern.sub(f"{Fore.YELLOW}{term}{Style.RESET_ALL}", content)
        
        formatted += f"\n{content}\n"
        formatted += f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n"
        return formatted

    def _parse_date_query(self, query):
        """Extract date information from query"""
        # Common date formats and keywords
        date_patterns = [
            r'\b\d{4}-\d{1,2}-\d{1,2}\b',  # YYYY-MM-DD
            r'\b\d{1,2}/\d{1,2}/\d{4}\b',   # MM/DD/YYYY
            r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|'
            r'Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|'
            r'Dec(?:ember)?)\s+\d{1,2}(?:st|nd|rd|th)?\s*,?\s*\d{4}\b'  # Month DD, YYYY
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                try:
                    return parser.parse(match.group())
                except ValueError:
                    continue
        return None

    def search(self, query, max_results=5):
        """
        Search emails using natural language query
        Supports:
        - Natural language queries
        - Sender/recipient search
        - Date-based search
        - Subject search
        - Content search
        - Combined searches
        """
        print(f"\n{Fore.BLUE}Searching for:{Style.RESET_ALL} {query}")
        
        # Extract potential search components
        query_lower = query.lower()
        
        # Check for sender/recipient specific queries
        sender_match = re.search(r'from\s+(\S+@\S+|\S+)', query_lower)
        recipient_match = re.search(r'to\s+(\S+@\S+|\S+)', query_lower)
        
        # Check for date-specific queries
        date = self._parse_date_query(query)
        
        # Get semantic search results
        semantic_results = self.retriever.search(query, k=max_results*2)
        result_ids = set()
        
        # Filter results based on specific criteria
        filtered_results = []
        for doc_id, score in semantic_results:
            email = self.emails[doc_id]
            
            # Apply sender filter
            if sender_match:
                sender = sender_match.group(1)
                if sender not in email.get('from', '').lower():
                    continue
                    
            # Apply recipient filter
            if recipient_match:
                recipient = recipient_match.group(1)
                if not any(recipient in r.lower() for r in email.get('to', [])):
                    continue
                    
            # Apply date filter
            if date:
                email_date = datetime.fromtimestamp(email['timestamp'] / 1000)
                if email_date.date() != date.date():
                    continue
            
            filtered_results.append((doc_id, score))
            if len(filtered_results) >= max_results:
                break
        
        # Display results
        if not filtered_results:
            print(f"{Fore.RED}No matching emails found.{Style.RESET_ALL}")
            return
        
        # Show results summary
        print(f"\n{Fore.GREEN}Found {len(filtered_results)} matching emails:{Style.RESET_ALL}")
        for i, (doc_id, score) in enumerate(filtered_results, 1):
            email = self.emails[doc_id]
            print(f"\n{Fore.YELLOW}[{i}]{Style.RESET_ALL}")
            print(f"From: {email.get('from', 'Unknown')}")
            print(f"Subject: {email.get('subject', 'No Subject')}")
            print(f"Date: {datetime.fromtimestamp(email['timestamp'] / 1000).strftime('%Y-%m-%d')}")
            print(f"Relevance Score: {score:.3f}")
        
        # Interactive viewing
        while True:
            choice = input(f"\n{Fore.GREEN}Enter number to view full email (or 'q' to quit):{Style.RESET_ALL} ")
            if choice.lower() == 'q':
                break
                
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(filtered_results):
                    doc_id = filtered_results[idx][0]
                    email = self.emails[doc_id]
                    
                    # Extract search terms for highlighting
                    search_terms = [word for word in query.split() 
                                  if word.lower() not in {'from', 'to', 'about', 'in', 'on', 'the'}]
                    
                    print(self._format_email(email, highlight_terms=search_terms))
                else:
                    print(f"{Fore.RED}Invalid choice. Please enter a number between 1 and {len(filtered_results)}.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")

def main():
    """Main function to run the email search system"""
    print(f"{Fore.CYAN}{'='*60}")
    print("Welcome to Email Search System")
    print("You can search using natural language queries like:")
    print("- 'Find emails about lunch plans'")
    print("- 'Show me emails from john about meetings'")
    print("- 'Find emails sent to bob.jones in October'")
    print(f"{'='*60}{Style.RESET_ALL}\n")
    
    search_system = EmailSearchSystem()
    
    while True:
        try:
            query = input(f"\n{Fore.GREEN}Enter your search query (or 'q' to quit):{Style.RESET_ALL} ")
            if query.lower() == 'q':
                break
            
            search_system.search(query)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}Thank you for using Email Search System!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

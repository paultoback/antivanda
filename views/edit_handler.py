# views/edit_handler.py

from datetime import datetime
from typing import Dict, List, Optional
import hashlib

class EditHandler:
    def __init__(self, config, blockchain_client):
        self.config = config
        self.blockchain_client = blockchain_client
        self.pending_edits = {}

    def submit_edit(self, article_id: str, edit_data: Dict) -> str:
        """
        Submit a new edit for review
        """
        edit_hash = self._generate_edit_hash(edit_data)
        timestamp = datetime.utcnow().isoformat()
        
        edit_record = {
            'article_id': article_id,
            'edit_hash': edit_hash,
            'timestamp': timestamp,
            'status': 'pending',
            'data': edit_data
        }
        
        self.pending_edits[edit_hash] = edit_record
        
        # Submit to blockchain
        tx_hash = self.blockchain_client.submit_edit(edit_hash, edit_record)
        return edit_hash

    def verify_edit(self, edit_hash: str) -> bool:
        """
        Verify an edit using AI and consensus
        """
        if edit_hash not in self.pending_edits:
            return False
            
        edit = self.pending_edits[edit_hash]
        
        # Verify through blockchain consensus
        consensus_result = self.blockchain_client.get_edit_consensus(edit_hash)
        
        if consensus_result['approved']:
            edit['status'] = 'approved'
            return True
        
        return False

    def _generate_edit_hash(self, edit_data: Dict) -> str:
        """
        Generate a unique hash for the edit
        """
        edit_string = f"{edit_data['article_id']}-{edit_data['timestamp']}-{edit_data['content']}"
        return hashlib.sha256(edit_string.encode()).hexdigest()

    def get_edit_history(self, article_id: str) -> List[Dict]:
        """
        Get edit history for an article
        """
        return self.blockchain_client.get_article_edits(article_id)

    def revert_edit(self, edit_hash: str) -> bool:
        """
        Revert an approved edit
        """
        if edit_hash not in self.pending_edits:
            return False
            
        revert_tx = self.blockchain_client.revert_edit(edit_hash)
        return revert_tx['success']
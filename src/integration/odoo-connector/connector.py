import os
import logging
import xmlrpc.client
from typing import Dict, List, Any, Optional, Union

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OdooConnector:
    """
    Connector for interacting with Odoo ERP system.
    """
    
    def __init__(self, url: str, db: str, username: str, api_key: str):
        """
        Initialize the Odoo connector.
        
        Args:
            url: Odoo server URL
            db: Database name
            username: Odoo username
            api_key: API key or password
        """
        self.url = url
        self.db = db
        self.username = username
        self.api_key = api_key
        
        # XML-RPC endpoints
        self.common_endpoint = f"{url}/xmlrpc/2/common"
        self.object_endpoint = f"{url}/xmlrpc/2/object"
        
        # Initialize connections
        self.common = xmlrpc.client.ServerProxy(self.common_endpoint)
        self.models = xmlrpc.client.ServerProxy(self.object_endpoint)
        
        # Authenticate and get user ID
        self.uid = self._authenticate()
        
    def _authenticate(self) -> int:
        """
        Authenticate with Odoo and get user ID.
        
        Returns:
            User ID for authenticated user
        """
        try:
            uid = self.common.authenticate(self.db, self.username, self.api_key, {})
            if not uid:
                raise ValueError("Authentication failed")
            logger.info(f"Successfully authenticated with Odoo as {self.username}")
            return uid
        except Exception as e:
            logger.error(f"Failed to authenticate with Odoo: {e}")
            raise
    
    def search_read(self, model: str, domain: List, fields: List[str] = None, 
                   limit: int = None, offset: int = 0, order: str = None) -> List[Dict]:
        """
        Search for records and read their data.
        
        Args:
            model: Odoo model name (e.g., 'res.partner')
            domain: Search domain
            fields: Fields to retrieve
            limit: Maximum number of records
            offset: Number of records to skip
            order: Order by clause
            
        Returns:
            List of records matching the search criteria
        """
        try:
            kwargs = {
                'offset': offset,
            }
            
            if fields:
                kwargs['fields'] = fields
            if limit:
                kwargs['limit'] = limit
            if order:
                kwargs['order'] = order
                
            results = self.models.execute_kw(
                self.db, self.uid, self.api_key,
                model, 'search_read',
                [domain], kwargs
            )
            
            logger.info(f"Retrieved {len(results)} records from {model}")
            return results
        except Exception as e:
            logger.error(f"Error searching {model}: {e}")
            raise
    
    def create(self, model: str, values: Dict[str, Any]) -> int:
        """
        Create a new record.
        
        Args:
            model: Odoo model name
            values: Field values for the new record
            
        Returns:
            ID of the created record
        """
        try:
            record_id = self.models.execute_kw(
                self.db, self.uid, self.api_key,
                model, 'create',
                [values]
            )
            
            logger.info(f"Created record {record_id} in {model}")
            return record_id
        except Exception as e:
            logger.error(f"Error creating record in {model}: {e}")
            raise
            
    def write(self, model: str, record_id: int, values: Dict[str, Any]) -> bool:
        """
        Update an existing record.
        
        Args:
            model: Odoo model name
            record_id: ID of the record to update
            values: Field values to update
            
        Returns:
            True if successful
        """
        try:
            result = self.models.execute_kw(
                self.db, self.uid, self.api_key,
                model, 'write',
                [[record_id], values]
            )
            
            logger.info(f"Updated record {record_id} in {model}")
            return result
        except Exception as e:
            logger.error(f"Error updating record {record_id} in {model}: {e}")
            raise
            
    def unlink(self, model: str, record_ids: Union[int, List[int]]) -> bool:
        """
        Delete records.
        
        Args:
            model: Odoo model name
            record_ids: ID or list of IDs to delete
            
        Returns:
            True if successful
        """
        if isinstance(record_ids, int):
            record_ids = [record_ids]
            
        try:
            result = self.models.execute_kw(
                self.db, self.uid, self.api_key,
                model, 'unlink',
                [record_ids]
            )
            
            logger.info(f"Deleted records {record_ids} from {model}")
            return result
        except Exception as e:
            logger.error(f"Error deleting records {record_ids} from {model}: {e}")
            raise
            
    def execute(self, model: str, method: str, args: List = None, kwargs: Dict = None) -> Any:
        """
        Execute a custom method on a model.
        
        Args:
            model: Odoo model name
            method: Method name to execute
            args: Positional arguments
            kwargs: Keyword arguments
            
        Returns:
            Result of the method call
        """
        args = args or []
        kwargs = kwargs or {}
        
        try:
            result = self.models.execute_kw(
                self.db, self.uid, self.api_key,
                model, method,
                args, kwargs
            )
            
            logger.info(f"Executed {method} on {model}")
            return result
        except Exception as e:
            logger.error(f"Error executing {method} on {model}: {e}")
            raise


# Example usage
if __name__ == "__main__":
    # These would normally be loaded from environment variables
    odoo = OdooConnector(
        url="https://example.odoo.com",
        db="example_db",
        username="admin",
        api_key="your_api_key"
    )
    
    # Example: Get customers
    customers = odoo.search_read(
        model='res.partner',
        domain=[('customer_rank', '>', 0)],
        fields=['name', 'email', 'phone'],
        limit=10
    )
    
    for customer in customers:
        print(f"Customer: {customer['name']}")
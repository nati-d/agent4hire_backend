from datetime import datetime, timedelta
import os
import requests
from dotenv import load_dotenv
from typing import Any, Dict, List, Optional, Union

# need to install the library to use for now it's not going to be 
# because we are not using and I am not sure if we will
# from intuitlib.client import AuthClient 
# # from intuitlib.enums import Scopes
# from intuitlib.exceptions import AuthClientError


class QuickBooksAPI:
    """
    A client for interacting with QuickBooks Online API.

    Attributes:
        company_id (str): The QuickBooks company ID.
        api_base_url (str): The base URL for QuickBooks API.
        client_id (str): The client ID for QuickBooks API.
        client_secret (str): The client secret for QuickBooks API.
        redirect_uri (str): The redirect URI for QuickBooks OAuth2.
        refresh_token (str): The refresh token for QuickBooks API.
        access_token (str): The access token for QuickBooks API.
        token_expiry (datetime): The expiration time of the access token.
        auth_client (AuthClient): The AuthClient instance for handling OAuth2.
    """

    def __init__(self) -> None:
        """Initialize the QuickBooksClient and load environment variables."""
        load_dotenv()

        # Configuration
        self.company_id: str = os.getenv("QB_COMPANY_ID")
        self.api_base_url: str = os.getenv("QB_API_BASE_URL")
        self.client_id: str = os.getenv("QB_CLIENT_ID")
        self.client_secret: str = os.getenv("QB_CLIENT_SECRET")
        self.redirect_uri: str = os.getenv("QB_REDIRECT_URI", "https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl")
        self.refresh_token: str = os.getenv("QB_REFRESH_TOKEN")

        # Initialize AuthClient
        self.auth_client: AuthClient = AuthClient(
            client_id=self.client_id,
            client_secret=self.client_secret,
            refresh_token=self.refresh_token,
            redirect_uri=self.redirect_uri,
            environment='production'  # or 'production'
        )

        # Access token and expiry
        self.access_token: Optional[str] = None
        self.token_expiry: Optional[datetime] = None

    def _get_authorization_url(self) -> str:
        """
        Generate the authorization URL for the user to log in to QuickBooks.

        Returns:
            str: The authorization URL.
        """
        print(self.__dict__)
        return self.auth_client.get_authorization_url(scopes=[Scopes.ACCOUNTING])

    def _exchange_code_for_tokens(self, auth_code: str, realm_id: str) -> None:
        """
        Exchange the authorization code for access and refresh tokens.

        Args:
            auth_code (str): The authorization code received from the callback.
        """
        try:
            self.auth_client.get_bearer_token(auth_code, realm_id)
            self.refresh_token = self.auth_client.refresh_token
            self.access_token = self.auth_client.access_token
            self.token_expiry = datetime.now() + timedelta(seconds=self.auth_client.expires_in)
            # Optionally, save tokens to environment or database
            print("Access Token:", self.access_token)
            print("Refresh Token:", self.refresh_token)
            return {
                'access_token': self.access_token,
                'refresh_token': self.refresh_token,
                'expires_in': self.auth_client.expires_in,
                'x_refresh_token_expires_in': self.auth_client.x_refresh_token_expires_in,
            }
        except AuthClientError as e:
            print(e.status_code, e.content, e.intuit_tid)
            raise

    def _refresh_access_token(self) -> str:
        """
        Refresh the access token using the refresh token.

        Returns:
            str: The new access token.
        """
        try:
            self.auth_client.refresh()
            self.access_token = self.auth_client.access_token
            self.token_expiry = datetime.now() + timedelta(seconds=self.auth_client.expires_in)
            return self.access_token
        except AuthClientError as e:
            print(e.status_code, e.content, e.intuit_tid)
            raise

    def _get_access_token(self) -> str:
        """
        Get the access token, refreshing it if necessary.

        Returns:
            str: The current access token.
        """
        if self.access_token is None or self.token_expiry is None or datetime.now() >= self.token_expiry:
            return self._refresh_access_token()
        return self.access_token

    def _api_client(self, endpoint: str = 'account', method: str = 'GET', data: Optional[Dict[str, Any]] = None) -> Union[Dict[str, Any], List[Any]]:
        """
        Make an API request to QuickBooks.

        Args:
            endpoint (str): The API endpoint to request. Defaults to 'account'.
            method (str): The HTTP method to use. Defaults to 'GET'.
            data (Optional[Dict[str, Any]]): The data to send in the request body. Defaults to None.

        Returns:
            Union[Dict[str, Any], List[Any]]: The JSON response from the API.
        """
        access_token = self._get_access_token()
        url = f"{self.api_base_url}/{self.company_id}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        response = requests.request(method, url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    # ACCOUNT FUNCTIONS
    def get_accounts(self) -> Union[Dict[str, Any], List[Any]]:
        """Retrieve all accounts."""
        return self._api_client('account', 'GET')

    def create_account(self, name: str = 'Default Account', account_type: str = 'Expense') -> Union[Dict[str, Any], List[Any]]:
        """
        Create a new account.

        Args:
            name (str): The name of the account. Defaults to 'Default Account'.
            account_type (str): The type of the account. Defaults to 'Expense'.

        Returns:
            Union[Dict[str, Any], List[Any]]: The JSON response from the API.
        """
        data = {
            "Name": name,
            "AccountType": account_type
        }
        return self._api_client('account', 'POST', data)

    # def update_account(self, account_id: str, updated_data: Optional[Dict[str, Any]] = None) -> Union[Dict[str, Any], List[Any]]:
    #     """
    #     Update an existing account.

    #     Args:
    #         account_id (str): The ID of the account to update. Defaults to 'default_account_id'.
    #         updated_data (Optional[Dict[str, Any]]): The data to update. Defaults to None.

    #     Returns:
    #         Union[Dict[str, Any], List[Any]]: The JSON response from the API.
    #     """
    #     if updated_data is None:
    #         updated_data = {}
    #     data = {
    #         "Id": account_id,
    #         **updated_data
    #     }
    #     return self._api_client(f'account/{account_id}', 'POST', data)

    # def delete_account(self, account_id: str = 'default_account_id') -> Union[Dict[str, Any], List[Any]]:
    #     """
    #     Delete an existing account.

    #     Args:
    #         account_id (str): The ID of the account to delete. Defaults to 'default_account_id'.

    #     Returns:
    #         Union[Dict[str, Any], List[Any]]: The JSON response from the API.
    #     """
    #     return self._api_client(f'account/{account_id}', 'DELETE')

    # TRANSACTION FUNCTIONS
    def get_transactions(self) -> Union[Dict[str, Any], List[Any]]:
        """
        Retrieve all transactions from QuickBooks.

        This method constructs a SQL-like query to fetch all transaction records
        from the QuickBooks API. It utilizes the `_api_client` method to make
        a POST request to the 'query' endpoint with the specified query.

        Returns:
            Union[Dict[str, Any], List[Any]]: The JSON response from the API,
            which contains the transaction data. The response can be a dictionary
            or a list, depending on the API's response structure.

        Example:
            transactions = api.get_transactions()
            for transaction in transactions.get('QueryResponse', {}).get('Transaction', []):
                print(transaction)
        """
        query = "SELECT * FROM Transaction"
        return self._api_client('query', 'POST', {"query": query})

    def create_transaction(self, transaction_type: str, amount: float = 0.0, account_id: str = 'default_account_id', category: str = 'General') -> Union[Dict[str, Any], List[Any]]:
        """
        Create a new transaction.

        Args:
            transaction_type (str): The type of the transaction. Defaults to 'journalentry'.
            amount (float): The amount of the transaction. Defaults to 0.0.
            account_id (str): The ID of the account for the transaction. Defaults to 'default_account_id'.
            category (str): The category of the transaction. Defaults to 'General'.

        Returns:
            Union[Dict[str, Any], List[Any]]: The JSON response from the API.
        """
        data = {
            "Amount": amount,
            "AccountRef": {
                "value": account_id
            },
            "Category": category
        }
        return self._api_client(transaction_type, 'POST', data)

    # def update_transaction(self, transaction_id: str, updated_data: Optional[Dict[str, Any]] = None) -> Union[Dict[str, Any], List[Any]]:
    #     """
    #     Update an existing transaction.

    #     Args:
    #         transaction_id (str): The ID of the transaction to update. Defaults to 'default_transaction_id'.
    #         updated_data (Optional[Dict[str, Any]]): The data to update. Defaults to None.

    #     Returns:
    #         Union[Dict[str, Any], List[Any]]: The JSON response from the API.
    #     """
    #     if updated_data is None:
    #         updated_data = {}
    #     data = {
    #         "Id": transaction_id,
    #         **updated_data
    #     }
    #     return self._api_client(f'transaction/{transaction_id}', 'POST', data)

    def delete_transaction(self, transaction_id: str) -> Union[Dict[str, Any], List[Any]]:
        """
        Delete an existing transaction.

        Args:
            transaction_id (str): The ID of the transaction to delete. Defaults to 'default_transaction_id'.

        Returns:
            Union[Dict[str, Any], List[Any]]: The JSON response from the API.
        """
        return self._api_client(f'transaction/{transaction_id}', 'DELETE')

    # BUDGET FUNCTIONS
    def get_budgets(self) -> Union[Dict[str, Any], List[Any]]:
        """Retrieve all budgets."""
        return self._api_client('budget', 'GET')

    # def create_budget(self, name: str = 'Default Budget', start_date: str = '2024-01-01', end_date: str = '2024-12-31', budget_details: Optional[List[Dict[str, Any]]] = None, category: str = 'General') -> Union[Dict[str, Any], List[Any]]:
    #     """
    #     Create a new budget.

    #     Args:
    #         name (str): The name of the budget. Defaults to 'Default Budget'.
    #         start_date (str): The start date of the budget. Defaults to '2024-01-01'.
    #         end_date (str): The end date of the budget. Defaults to '2024-12-31'.
    #         budget_details (Optional[List[Dict[str, Any]]]): The details of the budget. Defaults to None.
    #         category (str): The category of the budget. Defaults to 'General'.

    #     Returns:
    #         Union[Dict[str, Any], List[Any]]: The JSON response from the API.
    #     """
    #     if budget_details is None:
    #         budget_details = []
    #     data = {
    #         "Name": name,
    #         "StartDate": start_date,
    #         "EndDate": end_date,
    #         "BudgetDetails": budget_details,
    #         "Category": category
    #     }
    #     return self._api_client('budget', 'POST', data)

    # def update_budget(self, budget_id: str = 'default_budget_id', updated_data: Optional[Dict[str, Any]] = None) -> Union[Dict[str, Any], List[Any]]:
    #     """
    #     Update an existing budget.

    #     Args:
    #         budget_id (str): The ID of the budget to update. Defaults to 'default_budget_id'.
    #         updated_data (Optional[Dict[str, Any]]): The data to update. Defaults to None.

    #     Returns:
    #         Union[Dict[str, Any], List[Any]]: The JSON response from the API.
    #     """
    #     if updated_data is None:
    #         updated_data = {}
    #     data = {
    #         "Id": budget_id,
    #         **updated_data
    #     }
    #     return self._api_client(f'budget/{budget_id}', 'POST', data)

    def delete_budget(self, budget_id: str = 'default_budget_id') -> Union[Dict[str, Any], List[Any]]:
        """
        Delete an existing budget.

        Args:
            budget_id (str): The ID of the budget to delete. Defaults to 'default_budget_id'.

        Returns:
            Union[Dict[str, Any], List[Any]]: The JSON response from the API.
        """
        return self._api_client(f'budget/{budget_id}', 'DELETE')

    # COMPARISON FUNCTION
    def compare_budget_with_actual(self, budget_id: str = 'default_budget_id') -> None:
        """
        Compare a budget with actual transactions within its time frame.

        Args:
            budget_id (str): The ID of the budget to compare. Defaults to 'default_budget_id'.

        Returns:
            None: Prints the comparison results.
        """
        budgets = self.get_budgets()
        budget = next((b for b in budgets.get('Budget', []) if b['Id'] == budget_id), None)
        if not budget:
            print(f"Budget with ID {budget_id} not found.")
            return

        budget_details = budget.get('BudgetDetail', [])
        start_date = budget.get('StartDate', '2024-01-01')
        end_date = budget.get('EndDate', '2024-12-31')

        transactions = self.get_transactions()
        filtered_transactions = [
            t for t in transactions.get('QueryResponse', {}).get('Transaction', [])
            if start_date <= t.get('TxnDate', '2024-01-01') <= end_date
        ]

        actuals = {}
        for transaction in filtered_transactions:
            account_id = transaction['AccountRef'].get('value', 'default_account_id')
            category = transaction.get('Category', 'Uncategorized')
            amount = float(transaction['Amount'])
            if account_id not in actuals:
                actuals[account_id] = {}
            if category in actuals[account_id]:
                actuals[account_id][category] += amount
            else:
                actuals[account_id][category] = amount

        comparison = []
        for detail in budget_details:
            account_id = detail['AccountRef'].get('value', 'default_account_id')
            budgeted_amount = float(detail.get('Amount', 0.0))
            actual_amount = sum(actuals.get(account_id, {}).values())
            comparison.append({
                'AccountId': account_id,
                'BudgetedAmount': budgeted_amount,
                'ActualAmount': actual_amount,
                'Difference': budgeted_amount - actual_amount
            })

        for item in comparison:
            print(f"Account ID: {item['AccountId']}, Budgeted: {item['BudgetedAmount']}, Actual: {item['ActualAmount']}, Difference: {item['Difference']}")

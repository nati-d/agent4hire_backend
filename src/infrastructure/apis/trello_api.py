import os
from dotenv import load_dotenv 
from trello import TrelloClient 
from typing import Any, Dict, List

load_dotenv()

class TrelloAPI:
    """
    A class to interact with the Trello API to manage boards, lists, and cards.
    """

    def __init__(self):
        """
        Initializes the TrelloAPI client with the necessary credentials.
        """
        self.api_key = os.getenv('TRELLO_API_KEY')
        self.token = os.getenv('TRELLO_TOKEN')

        if not self.api_key or not self.token:
            raise ValueError("Trello API key or token not provided in environment variables.")

        self.client = TrelloClient(
            api_key=self.api_key,
            api_secret=None,
            token=self.token,
            token_secret=None
        )

    def get_boards(self) -> List[Dict[str, Any]]:
        """
        Fetch all boards for the authenticated user.

        Returns:
            List[Dict[str, Any]]: A list of board records.
        """
        boards = self.client.list_boards()
        return [{'id': board.id, 'name': board.name} for board in boards]

    def get_board(self, board_id: str) -> Dict[str, Any]:
        """
        Fetch details of a specific board by ID.

        Args:
            board_id (str): The ID of the board to fetch.

        Returns:
            Dict[str, Any]: The board details.
        """
        board = self.client.get_board(board_id)
        return {"id": board.id, "name": board.name}
    
    def update_board(self, board_id: str, name: str) -> Dict[str, Any]:
        """
        Update the name of a specific board.

        Args:
            board_id (str): The ID of the board to update.
            name (str): The new name for the board.

        Returns:
            Dict[str, Any]: The updated board details.
        """
        board = self.client.get_board(board_id)
        board.name = name
        board.save()
        return {"id": board.id, "name": board.name}

    def delete_board(self, board_id: str) -> Dict[str, str]:
        """
        Delete a specific board by ID.

        Args:
            board_id (str): The ID of the board to delete.

        Returns:
            Dict[str, str]: Confirmation of board deletion.
        """
        board = self.client.get_board(board_id)
        board.delete()
        return {"message": "Board deleted successfully"}

    def create_list(self, board_id: str, name: str) -> Dict[str, Any]:
        """
        Create a new list in a specific board.

        Args:
            board_id (str): The ID of the board where the list will be created.
            name (str): The name of the new list.

        Returns:
            Dict[str, Any]: The details of the created list.
        """
        board = self.client.get_board(board_id)
        trello_list = board.add_list(name)
        return {"id": trello_list.id, "name": trello_list.name}

    def get_lists(self, board_id: str) -> List[Dict[str, Any]]:
        """
        Fetch all lists in a specific board.

        Args:
            board_id (str): The ID of the board whose lists will be fetched.

        Returns:
            List[Dict[str, Any]]: A list of list records.
        """
        board = self.client.get_board(board_id)
        lists = board.list_lists()
        return [{'id': lst.id, 'name': lst.name} for lst in lists]
    
    def get_list(self, list_id: str) -> Dict[str, Any]:
        """
        Fetch details of a specific list by ID.

        Args:
            list_id (str): The ID of the list to fetch.

        Returns:
            Dict[str, Any]: The details of the fetched list.
        """
        trello_list = self.client.get_list(list_id)
        return {"id": trello_list.id, "name": trello_list.name}

    def update_list(self, list_id: str, name: str) -> Dict[str, Any]:
        """
        Update the name of a specific list by ID.

        Args:
            list_id (str): The ID of the list to update.
            name (str): The new name for the list.

        Returns:
            Dict[str, Any]: The updated list details.
        """
        trello_list = self.client.get_list(list_id)
        trello_list.name = name
        trello_list.save()
        return {"id": trello_list.id, "name": trello_list.name}

    def delete_list(self, list_id: str) -> Dict[str, str]:
        """
        Delete a specific list by ID.

        Args:
            list_id (str): The ID of the list to delete.

        Returns:
            Dict[str, str]: Confirmation of list deletion.
        """
        trello_list = self.client.get_list(list_id)
        trello_list.delete()
        return {"message": "List deleted successfully"}

    def create_card(self, list_id: str, name: str, desc: str = '') -> Dict[str, Any]:
        """
        Create a new card in a specific list.

        Args:
            list_id (str): The ID of the list where the card will be created.
            name (str): The name of the new card.
            desc (str, optional): The description of the card.

        Returns:
            Dict[str, Any]: The details of the created card.
        """
        trello_list = self.client.get_list(list_id)
        card = trello_list.add_card(name, desc)
        return {'id': card.id, 'name': card.name}

    def get_card(self, card_id: str) -> Dict[str, Any]:
        """
        Fetch details of a specific card by ID.

        Args:
            card_id (str): The ID of the card to fetch.

        Returns:
            Dict[str, Any]: The card details.
        """
        card = self.client.get_card(card_id)
        return {"id": card.id, "name": card.name}

    def update_card(self, card_id: str, name: str) -> Dict[str, Any]:
        """
        Update the name of a specific card.

        Args:
            card_id (str): The ID of the card to update.
            name (str): The new name for the card.

        Returns:
            Dict[str, Any]: The updated card details.
        """
        card = self.client.get_card(card_id)
        card.name = name
        card.save()
        return {"id": card.id, "name": card.name}

    def delete_card(self, card_id: str) -> Dict[str, Any]:
        """
        Delete a specific card by ID.

        Args:
            card_id (str): The ID of the card to delete.

        Returns:
            Dict[str, Any]: Confirmation of deletion.
        """
        card = self.client.get_card(card_id)
        card.delete()
        return {'message': 'Card deleted successfully'}

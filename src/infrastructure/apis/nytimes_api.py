from typing import Any, Dict, Literal, Optional

import requests


class NYTimes:
    """
    The New York Times, including article information, headlines, metadata, and even
    historical articles, by making requests through a set of defined commands, enabling
    them to integrate this news data into their applications or projects 
    """

    BASE_URL = "https://api.nytimes.com/svc"

    def __init__(self, key):
        self.API_KEY = key
    
    # Article Search

    def search_articles(
        self,
        query: str,
        begin_date: Optional[str] = None,
        end_date: Optional[str] = None,
        sort: Optional[str] = "relevance",
        page: Optional[int] = 0,
    ) -> Dict:
        """
        Look up articles by keyword. You can refine your search using filters and facets.

        :param query: Search term for the articles.
        :param begin_date: Start date for the search in YYYYMMDD format (optional).
        :param end_date: End date for the search in YYYYMMDD format (optional).
        :param sort: Sort order ("newest", "oldest", "relevance").
        :param page: Page number for pagination (optional).
        :return: Articles matching the search query.
        """
        params = {
            "q": query,
            "begin_date": begin_date,
            "end_date": end_date,
            "sort": sort,
            "page": page,
        }

        params = {k: v for k, v in params.items() if v is not None}

        endpoint = "articlesearch.json"
        return self.__make_get_request(f"{self.BASE_URL}/search/v2/{endpoint}", params)

    # Books API

    def get_list_names(self) -> Dict:
        """
        Get all the NYT Best Sellers list names.

        :return: A list of all available Best Sellers lists.
        """
        return self.__make_get_request(f"{self.BASE_URL}/books/v3/lists/names.json")

    def get_book_list_data(self, date: str = "current", list_name: str = "hardcover-fiction") -> Dict:
        """
        Get books on the Best Sellers list for a specific date and list name.

        :param date: Date of the list in YYYY-MM-DD format. Use 'current' for the latest list.
        :param list_name: Name of the Best Sellers list (e.g., "hardcover-fiction").
        :return: Books on the specified Best Sellers list.
        """
        endpoint = f"/{date}/{list_name}.json"
        return self.__make_get_request( f"{self.BASE_URL}/books/v3/{endpoint}", {})

    def get_full_overview(self, date: str = "current") -> Dict:
        """
        Get all books for all the Best Sellers lists for a specific date.

        :param date: Date of the list in YYYY-MM-DD format. Use 'current' for the latest list.
        :return: All books on all Best Sellers lists for the specified date.
        """
        endpoint = "lists/full-overview.json"
        params = {"published_date": date}
        return self.__make_get_request(f"{self.BASE_URL}/books/v3/{endpoint}", params)

    def get_best_seller_list_history(self, age_group: str, author: str, contributor : str, isbn: str, offset: int, price: str, publisher: str, title: str):
        """
        Get Best Seller list history.

        :param age_group: The target age group for the best seller.
        :param author: The author of the best seller.
        :param contributor: The author of the best seller, as well as other contributors such as the illustrator (to search or sort by author name only, use author instead).
        :param isbn: International Standard Book Number, 10 or 13 digits.
        :param offset: pagination offset.
        :param price: The publisher's list price of the best seller, including decimal point.
        :param publisher: The standardized name of the publisher.
        :param title: The title of the best seller.
        """
        endpoint = "list/best-sellers/history.json"
        params = {
            "age_group": age_group,
            "author": author,
            "contributor": contributor,
            "isbn": isbn,
            "offset": offset,
            "price": price,
            "publisher": publisher,
            "title": title
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.__make_get_request(f"{self.BASE_URL}/books/v3/{endpoint}", params)

    def get_overview(self, date: str = "current") -> Dict:
        """
        Get the top 5 books for all the Best Sellers lists for a specific date.

        :param date: Date of the list in YYYY-MM-DD format. Use 'current' for the latest list.
        :return: Top 5 books on all Best Sellers lists for the specified date.
        """
        endpoint = "/lists/overview.json"
        params = {"published_date": date}
        params = {k: v for k, v in params.items() if v is not None}

        return self.__make_get_request(f"{self.BASE_URL}/books/v3/{endpoint}", params)

    # Most Popular API

    def most_popular(self, period: int) -> Dict:
        """
        Returns an array of the most emailed articles on NYTimes.com for specified period of time (1 day, 7 days, or 30 days).
        """
        assert period in [1, 7, 30], "Period must be 1, 7, or 30 meaning (1 day, 7 days, or 30 days)."
        return self.__make_get_request(f"{self.BASE_URL}/mostpopular/v2/emailed/{period}.json")

    def most_shared(self, period: int) -> Dict:
        """
        Returns an array of the most emailed articles on NYTimes.com for specified period of time (1 day, 7 days, or 30 days).
        """
        assert period in [1, 7, 30], "Period must be 1, 7, or 30 meaning (1 day, 7 days, or 30 days)."
        return self.__make_get_request(f"{self.BASE_URL}/mostpopular/v2/shared/{period}.json")

    def most_shared_facebook(self, period: int) -> Dict:
        """
        Returns an array of the most emailed articles on NYTimes.com for specified period of time (1 day, 7 days, or 30 days).
        """
        assert period in [1, 7, 30], "Period must be 1, 7, or 30 meaning (1 day, 7 days, or 30 days)."
        return self.__make_get_request(f"{self.BASE_URL}/mostpopular/v2/shared/facebook/{period}.json")

    def most_viewed(self, period: int) -> Dict:
        """
        Returns an array of the most emailed articles on NYTimes.com for specified period of time (1 day, 7 days, or 30 days).
        """
        assert period in [1, 7, 30], "Period must be 1, 7, or 30 meaning (1 day, 7 days, or 30 days)."
        return self.__make_get_request(f"{self.BASE_URL}/mostpopular/v2/viewed/{period}.json")

    # Semantic API

    def get_concept( self, query: str, concept_type: str, specific_concept: str, fields="all") -> Dict:
        """
        Get information about a specific concept.

        :param query: The query to search for.
        :param concept_type: The concept to retrieve information about.
        :param specific_concept: The specific concept to retrieve information about.
        :param fields: The fields to include in the response. Options:
            all, pages, ticker_symbol, links, taxonomy, combinations, geocodes, article_list, scope_notes, search_api_query:

        :return: Information about the specified concept.
        """
        params = {
            "query": query,
            "fields": fields
        }
        return self.__make_get_request(
            f"{self.BASE_URL}/semantic/v2/concept/{concept_type}/{specific_concept}.json",
            params,
        )

    def search_concept(self, query: str, offset: int = 10, fields="all") -> Dict:
        """
        Search for a concept by query.
        """
        params = {
            "query": query,
            "offset": offset,
            "fields": fields
        }
        return self.__make_get_request(
            f"{self.BASE_URL}/semantic/v2/concept/search.json", params
        )

    # Top Stories API

    def get_top_stories(self, section: str) -> Dict:
        return self.__make_get_request(f"{self.BASE_URL}/topstories/v2/{section}.json")

    # Movie Reviews API

    def get_movie_critics(self, reviewer: str) -> Dict:
        """
        Get movie critics from the New York Times.

        :param reviewer: The name of the reviewer.
        :return: Movie critics.
        """
        endpoint = f"critics/{reviewer}.json"

        return self.__make_get_request(f"{self.BASE_URL}/movies/v2/{endpoint}")

    def get_movie_reviews(self, type: str, offset: str, order: str) -> Dict:
        """
        Get movie reviews.

        :param type: The type of reviews to retrieve.
        :param offset: The offset for pagination.
        :param order: The order of the results.

        :return: Movie reviews.
        """
        params = {"offset": offset, "order": order}
        params = {k: v for k, v in params.items() if v is not None}

        return self.__make_get_request(
            f"{self.BASE_URL}/movies/v2/reviews/{type}.json",
            params,
        )

    def search_movie_review(
        self,
        reviewer: str,
        query: str,
        critics_pick: bool = False,
        offset: int = 20,
        opening_date: str = "1930-01-01:1940-01-01",
        order: str = "by-opening-date",
        publication_date: str = "1930-01-01:1940-01-01",
    ) -> Dict:
        """
        Search for movie reviews.

        :param reviewer: The name of the reviewer.
        :param query: The search query.
        :param critics_pick: Whether
        :param offset: The offset for pagination.
        :param opening_date: The opening date range.
        :param order: The order of the results.
        :param publication_date: The publication date range.

        :return: Movie reviews matching the search criteria.
        """
        endpoint = "reviews/search.json"
        params = {
            "reviewer": reviewer,
            "query": query,
            "critics_pick": critics_pick,
            "offset": offset,
            "opening_date": opening_date,
            "order": order,
            "publication_date": publication_date,
        }

        params = {k: v for k, v in params.items() if v is not None}

        return self.__make_get_request(f"{self.BASE_URL}/movies/v2/{endpoint}", params)

    # Archive
    def get_archive(self, year, month):
        """
        Retrieve articles from the New York Times archive for a specific month and year.

        :param year: The year of the articles.
        :param month: The month of the articles.
        :return: Articles from the specified month and year.
        """
        return self.__make_get_request(f"{self.BASE_URL}/archive/v1/{year}/{month}.json")

    def __make_get_request(self, url, params: Dict[str, Any]={}) -> Dict:
        """
        Helper function to make a GET request to the API.

        :param params: Query parameters for the GET request.
        :return: API response as a JSON dictionary.
        """
        params["api-key"] = self.API_KEY
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}


if __name__ == "__main__":
    api_key = "APIKEY HERE"
    api = NYTimes(api_key)

    # Search for articles
    # results = api.search_articles(query="obama", sort="newest", page=1)

    results = api.get_list_names()
    print(results)

from typing import Any, Dict, Final, Mapping
from flask import current_app
import requests


class OpenAIReAPI:
    """
    A class to interact with the OpenAIRE API to access scholarly research data.

    The OpenAIRE Graph is one of the largest open scholarly record collections worldwide, key in fostering Open
    Science and establishing its practices in the daily research activities. It's populated out of data sources
    trusted by scientists,
    """

    BASE_URL: Final[str] = "https://api-beta.openaire.eu/graph"

    ############################
    # Research Products Endpoints
    ############################

    def search_research_products(
        self,
        search: str,  # search in the content
        type: str = "publication", # publication, dataset, software, or other
        page : int = 1,
        page_size : int = 3,  # changed from default of 10 to 3 to avoid huge responses
        sort_by : str = "popularity DESC",   # fieldname sortDirection
    ) -> Dict[str, Any]:
        """
        Search in the content of the research products.

        :param search: The search query
        :type search: str

        :param type: The type of the research product. One of publication, dataset, software, or other
        :type type: str

        :param page: The page number
        :type page: int

        :param page_size: The number of items per page
        :type page_size: int

        :return: The search results The type of the research product. One of publication, dataset, software, or other
        :rtype: Dict[str, Any]
        """
        return self.__make_get_request(
            endpoint="researchProducts",
            params={
                "search": search,
                "type": type,
                "page": page,
                "pageSize": page_size,
                "sortBy": sort_by,
            },
        )

    def search_research_products_by_title(
        self,
        title: str,  # search in the main title
        type: str = "publication",  # publication, dataset, software, or other
        page: int = 1,
        page_size: int = 3,  # changed from default of 10 to 3 to avoid huge responses
        sort_by: str = "popularity DESC",  # fieldname sortDirection
    ) -> Dict[str, Any]:
        """
        Search in the research product's main title.

        :param title: The title of the research product
        :type title: str

        :param type: The type of the research product. One of publication, dataset, software, or other
        :type type: str

        :param page: The page number
        :type page: int

        :param page_size: The number of items per page
        :type page_size: int

        :return: The search results The type of the research product. One of publication, dataset, software, or other
        :rtype: Dict[str, Any]
        """
        return self.__make_get_request(
            endpoint="researchProducts",
            params={
                "mainTitle": title,
                "type": type,
                "page": page,
                "pageSize": page_size,
                "sortBy": sort_by,
            },
        )

    def search_research_producrs_by_openaire_id(
        self,
        id: str,
    ) -> Dict[str, Any]:
        """
        Search for a research product by OpenAIRE ID.

        :param id: The OpenAIRE ID of the research product
        :type id: str

        :return: The search results
        :rtype: Dict[str, Any]
        """
        return self.__make_get_request(
            endpoint=f"researchProducts/{id}",
        )

    ############################
    # Organizations endpoints
    ############################

    def search_organization(
        self,
        search: str,
        country_code: str = "",
        page: int = 1,
        page_size: int = 10,
    ):
        """
        Search the content of the organization.

        :param search: The search query
        :type search: str

        :param country_code: The country code of the organization
        :type country_code: str

        :param page: The page number
        :type page: int

        :param page_size: The number of items per page
        :type page_size: int

        :return: The search results
        :rtype: Dict[str, Any]
        """
        return self.__make_get_request(
            endpoint="organizations",
            params={
                "search": search,
                "page": page,
                "pageSize": page_size,
                "countryCode": country_code,
            },
        )

    def search_organization_by_legal_name(
        self,
        legal_name: str,
        country_code: str = "",
        page: int = 1,
        page_size: int = 10,
    ) -> Dict[str, Any]:
        """
        Search the organization by legal name.

        :param legal_name: The legal name of the organization
        :type legal_name: str

        :param country_code: The country code of the organization
        :type country_code: str

        :param page: The page number
        :type page: int

        :param page_size: The number of items per page
        :type page_size: int

        :return: The search results
        :rtype: Dict[str, Any]
        """
        return self.__make_get_request(
            endpoint="organizations",
            params={
                "legalName": legal_name,
                "page": page,
                "pageSize": page_size,
                "countryCode": country_code,
            },
        )

    def search_organization_by_short_name(
        self,
        short_name: str,
        country_code: str = "",
        page: int = 1,
        page_size: int = 10,
    ) -> Dict[str, Any]:
        """
        Search the organization by short name. Organizations are identified by their short name, e.g., AAU for Addis Ababa University.

        :param short_name: The short name of the organization, e.g., `AAU` for Addis Ababa University
        :type short_name: str

        :param country_code: The country code of the organization
        :type country_code: str

        :param page: The page number
        :type page: int

        :param page_size: The number of items per page
        :type page_size: int

        :return: The search results
        :rtype: Dict[str, Any]
        """
        return self.__make_get_request(
            endpoint="organizations",
            params={
                "legalShortName": short_name,
                "page": page,
                "pageSize": page_size,
                "countryCode": country_code,
            },
        )

    def search_organization_by_id(
        self,
        id: str,
    ):
        """
        Search the organization by it's OpenAIRE id.

        :param id: The OpenAIRE ID of the organization
        :type id: str

        :return: The search results
        :rtype: Dict[str, Any]
        """
        return self.__make_get_request(
            endpoint=f"organizations/{id}",
        )

    ############################
    # Datasources Endpoints
    ############################

    def search_datasources(
        self,
        search: str,
        page: int = 1,
        page_size: int = 5,
    ) -> Dict[str, Any]:
        """
        Search the content of the data sources.

        :param search: The search query
        :type search: str

        :param page: The page number
        :type page: int

        :param page_size: The number of items per page
        :type page_size: int

        :return: The search results
        :rtype: Dict[str, Any]
        """
        return self.__make_get_request(
            endpoint="dataSources",
            params={
                "search": search,
                "page": page,
                "pageSize": page_size,
            },
        )

    def search_datasource_by_official_name(
        self,
        official_name: str,
        page: int = 1,
        page_size: int = 5,
    ) -> Dict[str, Any]:
        """
        Search the data source by official name.

        :param official_name: The official name of the data source
        :type official_name: str

        :return: The search result
        """
        return self.__make_get_request(
            endpoint="dataSources",
            params={
                "officialName": official_name,
                "page": page,
                "pageSize": page_size,
            },
        )

    def search_datasource_by_short_name(
        self,
        short_name: str,
        page: int = 1,
        page_size: int = 5,
    ) -> Dict[str, Any]:
        """
        Search the data source by short name.

        :param short_name: The short name of the data source
        :type short_name: str

        :return: The search result
        """
        return self.__make_get_request(
            endpoint="dataSources",
            params={
                "legalShortName": short_name,
                "page": page,
                "pageSize": page_size,
            },
        )

    def search_datasource_by_id(
        self,
        id: str,
    ):
        """
        Search the data source by it's OpenAIRE id.

        :param id: The OpenAIRE ID of the data source
        :type id: str

        :return: The search result
        """
        return self.__make_get_request(
            endpoint=f"dataSources/{id}",
        )

    ############################
    # Project Endpoints
    ############################

    def search_project(
        self,
        search: str,
        page: int = 1,
        page_size: int = 10,
        sort_by: str = "relevance DESC",
    ) -> Dict[str, Any]:
        """
        Search project by the content of the project.

        :param search: The search query
        :type search: str

        :param page: The page number
        :type page: int

        :param page_size: The number of items per page
        :type page_size: int

        :param sort_by: The fieldname and sort direction
        :type sort_by: str

        :return: The search results
        :rtype: Dict[str, Any]
        """
        return self.__make_get_request(
            endpoint="projects",
            params={
                "search": search,
                "page": page,
                "pageSize": page_size,
                "sortBy": sort_by,
            },
        )

    def search_project_by_title(
        self,
        title: str,
        page: int = 1,
        page_size: int = 10,
        sort_by: str = "relevance DESC",
    ):
        """
        Search project by the title of the project.

        :param title: The title of the project
        :type title: str

        :param page: The page number
        :type page: int

        :param page_size: The number of items per page
        :type page_size: int

        :param sort_by: The fieldname and sort direction
        :type sort_by: str

        :return: The search results
        """
        return self.__make_get_request(
            endpoint="projects",
            params={
                "title": title,
                "page": page,
                "pageSize": page_size,
                "sortBy": sort_by,
            },
        )

    def search_project_by_id(
        self,
        id: str,
    ):
        """
        Seach a project by it's OpenAIRE ID.

        :param id: The OpenAIRE ID of the project
        :type id: str

        :return: The search result
        """
        return self.__make_get_request(
            endpoint=f"projects/{id}",
        )

    def __make_get_request(
        self,
        endpoint: str,
        params: Mapping[str, str | int] = {},
        headers: Mapping[str, str] = {"accept": "application/json"},
    ) -> Dict:
        """Helper method to make a GET request to the Spotify API.

        Parameters:
            endpoint (str): The API endpoint to call.
            params (Dict): The query parameters for the request.

        Returns:
            :Dict[str, Any]: A dictionary containing the API response.
        """
        url = f"{self.BASE_URL}/{endpoint}"

        try:
            response = requests.get(
                url,
                params=params,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            current_app.logger.error(f"Error while making Openaire API call: {e}")
            return {"error": str(e)}


# Example Usage of the OpenAIRE API
if __name__ == "__main__":
    open_aire_api = OpenAIReAPI()

    """
    Uncomment the following code snippets to test the OpenAIRE API
    """

    # publications = open_aire_api.search_research_products(
    #     search="Machine Learning",
    #     type="publication",
    # )
    # print(publications)

    # publications = open_aire_api.search_research_products_by_title(
    #     title="Relativity Theory",
    #     type="publication",
    # )
    # print(publications)

    # organization = open_aire_api.search_organization("Addis Ababa")
    # print(organization)

    """
    Example Output:

    ```
    [
        {
            "legalShortName": "AAU",
            "legalName": "Addis Ababa University",
            "websiteUrl": "http://www.aau.edu.et/",
            "alternativeNames": [
                "Addis Ababa University",
                "Haile Selassie I University ",
                "University College of Addis Ababa",
                "AAU",
            ],
            "country": {"code": "ET", "label": "Ethiopia"},
            "id": "openorgs____::a5b84fec8726ece7330961325979fa02",
            "pid": [
                {"scheme": "mag_id", "value": "4537092"},
                {"scheme": "PIC", "value": "992842046"},
                {"scheme": "OrgRef", "value": "434092"},
                {"scheme": "ROR", "value": "https://ror.org/038b8e254"},
                {"scheme": "Wikidata", "value": "Q1238770"},
                {"scheme": "FundRef", "value": "501100007941"},
                {"scheme": "ISNI", "value": "0000000112505688"},
                {"scheme": "GRID", "value": "grid.7123.7"},
                {"scheme": "ISNI", "value": "0000000112505688"},
            ],
        },
        {
            "legalShortName": "ADDIS ABABA UNIVERSITY",
            "legalName": "ADDIS ABABA UNIVERSITY",
            "websiteUrl": None,
            "alternativeNames": None,
            "country": {"code": "UNKNOWN", "label": "Unknown"},
            "id": "pending_org_::8e23b1c56c93deabd628571536287b4e",
            "pid": None,
        },
        ...
    ]
    ```
    """

    # organization = open_aire_api.search_organization_by_id(
    #     "openorgs____::a5b84fec8726ece7330961325979fa02"
    # )

    # organization = open_aire_api.search_organization_by_legal_name(
    #     "Addis Ababa University"
    # )

    # organization = open_aire_api.search_organization_by_short_name("AAU", country_code="ET")

    # print(organization)

    # search_id = "doi_dedup___::a55b42c0d32a4a24cf99e621623d110e"
    # print(open_aire_api.search_research_producrs_by_id(search_id))

    # datasources = open_aire_api.search_datasources("Addis Ababa University")
    # print(datasources)

    # datasource = open_aire_api.search_datasource_by_id("issn___print::22c514d022b199c346e7f29ca06efc95")

    # print(datasource)

    # project = open_aire_api.search_project_by_id("corda__h2020::70ea22400fd890c5033cb31642c4ae68")
    # print(project)

    # projects = open_aire_api.search_project("Open Scholarship")
    # print(projects)

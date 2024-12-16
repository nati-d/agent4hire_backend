import requests

class OpenCitationsAPI:
    BASE_URL = "https://opencitations.net/index/api/v1"

    @staticmethod
    def get_citation_count(doi: str):
        """
        Retrieve the number of incoming citations for a given DOI.

        :param doi: The DOI of the target paper.
        :return: JSON response with the citation count.
        """
        endpoint = f"{OpenCitationsAPI.BASE_URL}/citation-count/{doi}"
        response = requests.get(endpoint)
        return response.json()

    @staticmethod
    def get_reference_count(doi: str):
        """
        Retrieve the number of references (outgoing citations) for a given DOI.

        :param doi: The DOI of the target paper.
        :return: JSON response with the reference count.
        """
        endpoint = f"{OpenCitationsAPI.BASE_URL}/reference-count/{doi}"
        response = requests.get(endpoint)
        return response.json()

    @staticmethod
    def get_references(doi: str):
        """
        Retrieve the references (outgoing citations) for a given DOI.

        :param doi: The DOI of the target paper.
        :return: JSON response with the references.
        """
        endpoint = f"{OpenCitationsAPI.BASE_URL}/references/{doi}"
        response = requests.get(endpoint)
        return response.json()

    @staticmethod
    def get_citations(doi: str):
        """
        Retrieve the citations (incoming citations) for a given DOI.

        :param doi: The DOI of the target paper.
        :return: JSON response with the citations.
        """
        endpoint = f"{OpenCitationsAPI.BASE_URL}/citations/{doi}"
        response = requests.get(endpoint)
        return response.json()

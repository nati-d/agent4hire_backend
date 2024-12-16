from typing import Any, Dict
from scholarly import scholarly, ProxyGenerator


class ScholarlyApi:
    """
    ScholarlyApi class is used to retrieve author and publication information from Google Scholar.
    """

    def __init__(self):
        """
        Initializes the ScholarlyApi class by creating a ProxyGenerator object and setting the timeout and wait time.
        We're using the proxy generator to avoid our ip getting blocked by Google Scholar since we could make multiple requests.
        """
        self.pg = ProxyGenerator()
        self.pg.FreeProxies(timeout=20, wait_time=120)
        self.scholarly = scholarly

    def search_author(self, author_name: str) -> Dict[str, Any]:
        """
        Search for an author by name.
        
        :param author_name: Name of the author to search for.
        :return: Author information.
        """
        search_query = self.scholarly.search_author(author_name) # type: ignore
        author = next(search_query) # type: ignore
        return author

    def search_publication(self, publication_title: str) -> Dict[str, Any]:
        """
        Search for a publication by title.

        :param publication_title: Title of the publication to search for.
        :return: Publication information.
        """
        search_query = self.scholarly.search_pubs(publication_title)
        publication = next(search_query)
        return publication # type: ignore

    def search_author_id(self, author_id: str) -> Dict[str, Any]:
        """
        Search for an author by ID.

        :param author_id: ID of the author to search for.
        :return: Author information.
        """
        author = self.scholarly.search_author_id(author_id)
        return author # type: ignore

    def search_organization(self, organization: str) -> Dict[str, Any]:
        """
        Search for an organization.

        :param organization: Name of the organization to search for.
        :return: Organization information.
        """
        search_query = self.scholarly.search_org(organization)
        organization = next(search_query) # type: ignore
        return organization # type: ignore

    def search_author_by_organization(self, organization: int) -> Dict[str, Any]:
        """
        Search for an author by organization.

        :param organization: Name of the organization to search for.
        :return: Author information.
        """
        search_query = self.scholarly.search_author_by_organization(organization)
        author = next(search_query) # type: ignore
        return author

    def search_keyword(self, keyword: str) -> Dict[str, Any]:
        """
        Search for a keyword.
        
        :param keyword: Keyword to search for.
        :return: Keyword information.
        """
        search_query = self.scholarly.search_keyword(keyword)
        keyword = next(search_query)  # type: ignore
        return keyword  # type: ignore


# Example Usage of the Scholarly API
if __name__ == "__main__":
    scholarly_api = ScholarlyApi()
    author = scholarly_api.search_author("Albert Einstein")
    print(author)
    """
    Output:

    ```
    {
        'container_type': 'Author',
        'filled': [],
        'source': <AuthorSource.SEARCH_AUTHOR_SNIPPETS: 'SEARCH_AUTHOR_SNIPPETS'>,
        'scholar_id': '6i1CnWQAAAAJ',
        'url_picture': 'https://scholar.google.com/citations?view_op=medium_photo&user=6i1CnWQAAAAJ',
        'name': 'Albert Einstein',
        'affiliation': 'Ankara University',
        'email_domain': '@ogrenci.ankara.edu.tr',
        'interests': ['general relativity', 'special relativity'],
        'citedby': 199153
    }
    ```
    """

    publication = scholarly_api.search_publication(
        "A New Determination of Molecular Dimensions"
    )

    print(publication)
    """
    Output:

    ```
    {
        'container_type': 'Publication',
        'source': <PublicationSource.PUBLICATION_SEARCH_SNIPPET: 'PUBLICATION_SEARCH_SNIPPET'>,
        'bib': {
            'title': 'A new determination of molecular dimensions',
            'author': ['A Einstein'],
            'pub_year': '1906',
            'venue': 'Annln., Phys.',
            'abstract': 'A New Determination of Molecular Dimensions | CiNii Research  A New Determination of  Molecular Dimensions'
        },
        'filled': False,
        'gsrank': 1, 'pub_url': 'https://cir.nii.ac.jp/crid/1573950400755209088',
        'author_id': ['qc6CJjYAAAAJ'],
        'url_scholarbib': '/scholar?hl=en&q=info:FyhknoZBfDoJ:scholar.google.com/&output=cite&scirp=0&hl=en',
        'url_add_sclib': '/citations?hl=en&xsrf=&continue=/scholar%3Fq%3DA%2BNew%2BDetermination%2Bof%2BMolecular%2BDimensions%26hl%3Den%26as_sdt%3D0,33&citilm=1&update_op=library_add&info=FyhknoZBfDoJ&ei=oB0zZ-zDL8y_y9YPzt6E4Aw&json=',
        'num_citations': 1289,
        'citedby_url': '/scholar?cites=4214315397750728727&as_sdt=5,33&sciodt=0,33&hl=en',
        'url_related_articles': '/scholar?q=related:FyhknoZBfDoJ:scholar.google.com/&scioq=A+New+Determination+of+Molecular+Dimensions&hl=en&as_sdt=0,33'
    }
    ```
    """

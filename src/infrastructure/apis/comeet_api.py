import requests

class ComeetApi:
    def __init__(self, api_key: str, company_id: str):
        """
        Initialize the ComeetApi class.
        :param api_key: Your Comeet API key.
        :param company_id: The unique identifier for your company in Comeet.
        """
        self.api_key = api_key
        self.company_id = company_id
        self.base_url = f"https://api.comeet.co/{self.company_id}"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def get_positions(self):
        """
        Retrieve all positions in the company.
        :return: JSON response with position data.
        """
        url = f"{self.base_url}/positions"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_position_details(self, position_uid: str):
        """
        Retrieve details for a specific position.
        :param position_uid: Unique identifier of the position.
        :return: JSON response with position details.
        """
        url = f"{self.base_url}/positions/{position_uid}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def create_candidate(self, position_uid: str, candidate_data: dict):
        """
        Add a candidate to a position.
        :param position_uid: Unique identifier of the position.
        :param candidate_data: Dictionary containing candidate details.
        :return: JSON response with the created candidate data.
        """
        url = f"{self.base_url}/positions/{position_uid}/candidates"
        response = requests.post(url, headers=self.headers, json=candidate_data)
        response.raise_for_status()
        return response.json()

    def get_candidates(self, position_uid: str):
        """
        Retrieve all candidates for a position.
        :param position_uid: Unique identifier of the position.
        :return: JSON response with candidate data.
        """
        url = f"{self.base_url}/positions/{position_uid}/candidates"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_candidate_details(self, candidate_uid: str):
        """
        Retrieve details of a specific candidate.
        :param candidate_uid: Unique identifier of the candidate.
        :return: JSON response with candidate details.
        """
        url = f"{self.base_url}/candidates/{candidate_uid}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def update_candidate_status(self, candidate_uid: str, status_data: dict):
        """
        Update the status of a candidate.
        :param candidate_uid: Unique identifier of the candidate.
        :param status_data: Dictionary containing status update information.
        :return: JSON response with the updated candidate data.
        """
        url = f"{self.base_url}/candidates/{candidate_uid}/status"
        response = requests.put(url, headers=self.headers, json=status_data)
        response.raise_for_status()
        return response.json()

    def get_hiring_managers(self):
        """
        Retrieve a list of hiring managers in the company.
        :return: JSON response with hiring manager data.
        """
        url = f"{self.base_url}/hiring/managers"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_interview_templates(self):
        """
        Retrieve available interview templates.
        :return: JSON response with interview template data.
        """
        url = f"{self.base_url}/interviews/templates"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def schedule_interview(self, candidate_uid: str, interview_data: dict):
        """
        Schedule an interview for a candidate.
        :param candidate_uid: Unique identifier of the candidate.
        :param interview_data: Dictionary containing interview details.
        :return: JSON response with scheduled interview data.
        """
        url = f"{self.base_url}/candidates/{candidate_uid}/interviews"
        response = requests.post(url, headers=self.headers, json=interview_data)
        response.raise_for_status()
        return response.json()

    def get_reports(self):
        """
        Retrieve reports about hiring activities.
        :return: JSON response with report data.
        """
        url = f"{self.base_url}/reports"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

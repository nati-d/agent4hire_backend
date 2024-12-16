from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
import requests
import os


class GoogleFormApi:
    def __init__(self, credentials_path, api_name="forms", api_version="v1"):
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=["https://www.googleapis.com/auth/forms"]
        )
        self.service = build(api_name, api_version, credentials=self.credentials)

    def create_form(self, title, description):
        form_body = {
            "info": {
                "title": title,
                "description": description
            }
        }
        form = self.service.forms().create(body=form_body).execute()
        return form

    def add_question(self, form_id, question_text, question_type="SHORT_ANSWER"):
        question_body = {
            "requests": [
                {
                    "createItem": {
                        "item": {
                            "title": question_text,
                            "questionItem": {
                                "question": {
                                    "required": True,
                                    "textQuestion": {
                                        "paragraph": False if question_type == "SHORT_ANSWER" else True
                                    }
                                }
                            }
                        },
                        "location": {"index": 0}
                    }
                }
            ]
        }
        response = self.service.forms().batchUpdate(formId=form_id, body=question_body).execute()
        return response

    def get_form_responses(self, form_id):
        responses = self.service.forms().responses().list(formId=form_id).execute()
        return responses

    def update_form_title(self, form_id, new_title):
        update_body = {
            "requests": [
                {
                    "updateFormInfo": {
                        "info": {
                            "title": new_title
                        },
                        "updateMask": "title"
                    }
                }
            ]
        }
        response = self.service.forms().batchUpdate(formId=form_id, body=update_body).execute()
        return response

   






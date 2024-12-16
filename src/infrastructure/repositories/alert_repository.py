from typing import List, Optional
from google.cloud import firestore
from domain.models.alert import Alert


class AlertRepository:
    def __init__(self):
        self.database = firestore.Client(database="agent-square")
        self.collection_name = "alerts"

    def create(self, alert: Alert) -> Alert:
        try:
            self.database.collection(self.collection_name).document(alert.id).set(
                alert.to_dict()
            )
            return alert
        except Exception as e:
            raise e

    def get_by_id(self, alert_id: str) -> Optional[Alert]:
        try:
            alert = (
                self.database.collection(self.collection_name).document(alert_id).get()
            )
            return Alert.from_dict(alert.to_dict())  # type: ignore

        except Exception as e:
            raise e

    def get_all(self) -> List[Alert]:
        try:
            alerts = self.database.collection(self.collection_name).stream()
            return [Alert.from_dict(alert.to_dict()) for alert in alerts]
        except Exception as e:
            raise e

    def update(self, alert: Alert) -> Alert:
        try:
            self.database.collection(self.collection_name).document(alert.id).update(
                alert.to_dict()
            )
            return alert
        except Exception as e:
            raise e

    def delete(self, alert: Alert) -> None:
        try:
            self.database.collection(self.collection_name).document(alert.id).delete()
        except Exception as e:
            raise e

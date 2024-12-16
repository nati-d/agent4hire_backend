
from backend.src.domain.models.alert import Alert
from backend.src.infrastructure.repositories.alert_repository import AlertRepository


class AlertUsecase:
    def __init__(self, alert_repo: AlertRepository):
        self.alert_repo = alert_repo
    
    def get_alerts(self):
        return self.alert_repo.get_all()

    def get_alert_by_id(self, alert_id: str):
        return self.alert_repo.get_by_id(alert_id)

    def store_alert(self, alert: Alert):
        return self.alert_repo.create(alert)

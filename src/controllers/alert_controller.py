from flask import Request, Response
from backend.src.domain.models.alert import AlertState
from backend.src.usecases.alert_usercase import AlertUsecase


class AlertController:
    def __init__(self, alert_usecase: AlertUsecase):
        self.alert_service = alert_usecase

    def get_alerts(self, request: Request) -> Response:
        alerts = self.alert_service.get_alerts()
        return Response({"alerts": [alert.to_dict() for alert in alerts]})

    def dismiss_alert(self, request: Request) -> Response:
        alert_id = request.get("alert_id")  # type: ignore

        alert = self.alert_service.get_alert_by_id(alert_id)
        if not alert:
            return Response(status=404)

        alert.state = AlertState.DISMISSED
        self.alert_service.store_alert(alert)
        return Response(alert.to_dict())

from enum import Enum
from domain.models.kpi import KPI

class Frequency(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"
    NOT_REQUIRED = "not_required"

class Module:
    def __init__(self, module: str, kpis: list[KPI], frequency: str, apis: list[str] = []):
        self.module = module
        self.kpis = kpis
        self.frequency = frequency
        self.apis = apis
    def to_dict(self) -> dict:
        return {
            "module": self.module,
            "kpis": [kpi.to_dict() for kpi in self.kpis],
            "frequency": self.frequency,
            "apis": self.apis
        }
    
    @staticmethod
    def from_dict(module_data: dict) -> "Module":
        return Module(
            module=module_data["module"],
            kpis=[KPI.from_dict(kpi_data) for kpi_data in module_data["kpis"]],
            frequency=module_data["frequency"],
            apis=module_data["apis"]
        )

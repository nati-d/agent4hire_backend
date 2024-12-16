from typing import Any, Dict


class KPI:
    def __init__(self, kpi: str, expected_value: str):
        self.kpi = kpi
        self.expected_value = expected_value

    def to_dict(self) -> Dict[str, Any]:
        return {
            "kpi": self.kpi,
            "expected_value": self.expected_value
        }
    
    @staticmethod   
    def from_dict(kpi_data: Dict[str, Any]) -> "KPI":
        return KPI(
            kpi=kpi_data["kpi"],
            expected_value=kpi_data["expected_value"]
        )
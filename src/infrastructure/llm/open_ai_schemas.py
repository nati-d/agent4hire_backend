from pydantic import BaseModel
from typing import List, Dict

class StringSchema(BaseModel):
  string: str


class BooleanSchema(BaseModel):
  boolean: bool


class ArraySchema(BaseModel):
  array: list[str]
  
class StepSchema(BaseModel):
    steps: Dict[str, str]
    
    class Config:
        json_schema_extra = {
            "required": ["steps"]  # List of keys that are required, in this case, steps
        }


class AnswersScehma(BaseModel):
  answers: list[str]


class KpiSchema(BaseModel):
  kpi: str
  expected_value: str


class ReportSchema(BaseModel):
  user_persona: str
  specific_needs: list[str]
  kpis: list[KpiSchema]


class ModuleSchema(BaseModel):
  module: str
  frequency: str


class GoalSchema(BaseModel):
  goal: str
  kpis: list[KpiSchema]


class SubGoalSchema(BaseModel):
  sub_goal: str
  kpis: list[KpiSchema]


class WorkstreamSchema(BaseModel):
  workstream: str
  frequency: str
  kpis: list[KpiSchema]


class subgoals_schema(BaseModel):
  subgoals: list[SubGoalSchema]


class WorkstreamsSchema(BaseModel):
  workstreams: list[WorkstreamSchema]


class goals_schema(BaseModel):
  goals: list[GoalSchema]


class ModulesSchema(BaseModel):
  modules: list[ModuleSchema]
  

report_schema = {
    "type": "json_schema",
    "json_schema": {
        "name": "report_schema",
        "schema": {
            "type": "object",
            "properties": {
                "user_persona": {
                    "description":
                    "The persona of the user for whom the agent is created.",
                    "type": "string"
                },
                "specific_needs": {
                    "description":
                    "The specific needs the user has for the agent.",
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
                "kpis": {
                    "description":
                    "List of KPIs and their expected values for the agent.",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "kpi": {
                                "description": "The name of the KPI.",
                                "type": "string"
                            },
                            "expected_value": {
                                "description":
                                "The expected value of the KPI.",
                                "type": "string"
                            }
                        },
                        "required": ["kpi", "expected_value"],
                        "additionalProperties": False
                    }
                }
            },
            "required": ["user_persona", "specific_needs", "kpis"],
            "additionalProperties": False
        }
    }
}
workstreams_schema = {
    "type": "json_schema",
    "json_schema": {
        "name": "workstreams_schema",
        "schema": {
            "type": "object",
            "properties": {
                "workstreams": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "workstream": {
                                "description": "The name of the workstream.",
                                "type": "string"
                            },
                            "frequency": {
                                "description":
                                "The frequency at which this workstream occurs.",
                                "type": "string"
                            },
                            "kpis": {
                                "description":
                                "List of KPIs and their expected values for the workstream.",
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "kpi": {
                                            "description":
                                            "The name of the KPI.",
                                            "type": "string"
                                        },
                                        "expected_value": {
                                            "description":
                                            "The expected value for the KPI.",
                                            "type": "string"
                                        }
                                    },
                                    "required": ["kpi", "expected_value"],
                                    "additionalProperties": False
                                }
                            }
                        },
                        "required": ["workstream", "frequency", "kpis"],
                        "additionalProperties": False
                    }
                }
            },
            "required": ["workstreams"],
            "additionalProperties": False
        }
    }
}

modules_schema = {
    "type": "json_schema",
    "json_schema": {
        "name": "modules_schema",
        "schema": {
            "type": "object",
            "properties": {
                "modules": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "module": {
                                "description": "The name of the module.",
                                "type": "string"
                            },
                            "frequency": {
                                "description":
                                "The frequency at which this module is used or occurs.",
                                "type": "string"
                            }
                        },
                        "required": ["module", "frequency"],
                        "additionalProperties": False
                    }
                }
            },
            "required": ["modules"],
            "additionalProperties": False
        }
    }
}



api_tree_schema = {
           "type": "json_schema",
           "json_schema": {
               "name" : "next_branch_schema",
               "schema": {
               "type": "object",
               "properties": {
                   "chosen_option": {
                       "type": "string",
                       "description": "The selected option based on the query."
                   },
                   "confidence_score": {
                       "type": "number",
                       "description": "The confidence score for the chosen option."
                   },
                   "score_reason": {
                       "type": "string",
                       "description": "The descritpion of why the score was given for the chosen endpint"
                   }
               },
               "required": ["chosen_option", "confidence_score","score_reason"],
               "additionalProperties": False
           }
        }
       }

step_schema = {
           "type": "json_schema",
           "json_schema": {
               "name" : "regenerated_step_schema",
               "schema": {
               "type": "object",
               "properties": {
                   "new_step": {
                       "type": "string",
                       "description": "The step with the same structure as before."
                   }
               },
               "required": ["new_step"],
               "additionalProperties": False
           }
        }
       }


summary_schema= {
           "type": "json_schema",
           "json_schema": {
               "name" : "execution_summary",
               "schema": {
               "type": "object",
               "properties": {
                   "summary": {
                       "type": "string",
                       "description": "The summary of the general execution"
                   }
               },
               "required": ["summary"],
               "additionalProperties": False
           }
        }
       }







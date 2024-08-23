system_prompt = """For the given question, make plans that can solve for the question answer step by step. 
For each plan, indicate which external function (with its parameters) to call in order to retrieve evidence. 
You must store the evidence into a variable #E that can be called by later plans (functions).

Functions can be one of the following functions:

def get_patients() -> List[Patient]:
    ""
    class Patient:
        ""
        ID of the patient. You can use this to join with other tables.
        ""
        id: str

        ""
        First name of the patient. This should not be used to uniquely identify a patient.
        ""
        first: str

        ""
        Last name of the patient. This should not be used to uniquely identify a patient.
        ""
        last: str

        ""
        City name of where the patient lives.
        ""
        city: str

    Returns a list of all patients.

    Example: patients = get_patients()
    ""
    pass

def get_allergies() -> List[Allergy]:
    ""
    class Allergy:
        ""
        Start date of the allergy
        ""
        start_date: datetime

        ""
        End date of the allergy
        ""
        end_date: Optional[datetime]

        ""
        ID of the patient. 
        ""
        patient_id: str

    Returns a list of all allergies instances.

    Example: allergies = get_allergies()
    ""
    pass

def get_immunization() -> List[Immunization]:
    ""
    class Immunization:
        date: datetime

        patient_id: integer

        encounter_id: integer

        ""
        ID of the immunization. You can use this to join
        ""
        id: integer

        description: string

        base_cost: float
    ""
    pass

def filter(list: List[object], keys: List[str], values: List[str]) -> List[object]:
    ""
    Returns a new list with filtered elements based on keys and values.

    Example: filtered_shapes = filter(shapes, keys=["color"], values=["blue"])
    ""
    pass

def count(list: List) -> integer:
    ""
    Returns the number of elements in the list.

    Example: n_elements = count(shapes)
    ""
    pass

class JoinMode(Enum):
    INNER = 1
    LEFT = 2
    RIGHT = 3
    OUTER = 4

def join(a: List, b: List, left_key: str, right_key: str, how: JoinMode) -> List:
    ""
    Joins/merges two lists based on a respective key/field for each.

    Parameters "a" and "b" are required and need to be provided for all calls.

    Parameters "a" and "b" should be evidence variables starting with "#E"

    Example: #E3 = join(a="#E1", b="#E2", left_key="abc", left_key="xyz", how=JoinMode.INNER)
    ""
    pass

class SortOrder(Enum):
    ASCENDING = 1
    DESCENDING = 2

def order_by(list: List, key: str, value: SortOrder) -> List:
    ""
    Orders the list based on a key/field

    Example: shapes = order_by(shapes, "size", SortOrder.ASCENDING)
    ""
    pass

class GroupByAggregation(Enum):
    COUNT = 1
    MEAN = 2

def group_by(list: List, group_key: str, aggregation_key: Optional[str], aggregation: GroupByAggregation) -> List:
    ""
    Groups the list based on a key and an aggregation.

    If you use a GroupByAggregation.COUNT aggregation, a "count" column is added to the result, otherwise, the column name being aggregated persists.

    Example: shapes = group_by(shapes, "size", "color", GroupByAggregation.COUNT)
    ""
    pass

def limit(list: List, k: Integer) -> List:
    ""
    Returns the top k elements of a list

    Example: shapes = limit(shapes, 5)
    ""
    pass

def distinct(list: List, key: str) -> List:
    ""
    Returns the distinct values for the key attribute in the list
    ""
    pass

def select(list: List, keys: List[str]) -> List:
    ""
    Keeps only certain columns from the list. Useful to drop unnecessary columns.
    ""
    pass

Describe your plans with rich details. Each Plan should result in only one #E and may use multiple #E.

Notice that in order for a plan to use an evidence #E, that evidence should have been produced by a PREVIOUS plan.

'None' values should be represented by null"""

plan_tool = {
    "toolSpec": {
        "name": "execute_plan",
        "description": "Executes the plan to arrive at the answer for the question",
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {
                    "plans": {
                        "type": "array",
                        "description": "List of each plan in order they need to be executed",
                        "items": {
                            "type": "object",
                            "properties": {
                                "function_name": {
                                    "type": "string",
                                    "description": "The name of the function to call",
                                },
                                "parameters": {
                                    "type": "array",
                                    "description": "Name of the parameters to use",
                                },
                                "parameter_values": {
                                    "type": "array",
                                    "description": "Values for the respective 'parameters'. You may use evidence (#E1, #E2...) variables here. You can also use literal values.",
                                },
                                "evidence_number": {
                                    "type": "integer",
                                    "description": "The number of the evidence variable that holds the result of this function call",
                                }
                            },
                            "required": ["function_name", "parameters", "parameter_values", "evidence_number"]
                        }
                    },
                },
                "required": ["plans"],
            }
        },
    }
}

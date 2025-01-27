
# Domain Model
from dataclasses import dataclass

@dataclass
class EmployeeLevelDomain:
    title: str
    version: int = 1

    
from enum import Enum
class MemoryType(Enum):
    OBSERVATION = "observation"
    DAILYPLAN = "dailyplan"
    HOURPLAN = "hourplan"
    ACTION = "action"
    REFLECTION = "reflection"

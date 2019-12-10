"""
A meta class is a class of class whose instances are classes here these are not exactly meta classes but 
these class instances are generated for other instances
"""

from enum import Enum
from pydantic import BaseModel

def __init__(self):
    pass

class KeyTypes(Enum):
    primarykey = "HASH"
    secondarykey = "RANGE"

class AttributeTypes(Enum):
    String = "S"
    Integer = "N"
    Boolean = "B"

class MetaKeySchema(BaseModel):
    AttributeName: str
    KeyType: KeyTypes
    AttributeType: AttributeTypes

class MetaAttributeDef(BaseModel):
    AttributeName: str
    AttributeType: AttributeTypes

class MetaProvisionedThroughput(BaseModel):
    ReadCapacityUnits: int = 10
    WriteCapacityUnits: int = 10
    
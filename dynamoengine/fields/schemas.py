from pydantic import BaseModel


class MetaSchema(BaseModel):
    AttributeName: str
    KeyType: str
    AttributeType: str

    def update_name(self, name):
        self.AttributeName = name


class AttributeSchema(BaseModel):
    AttributeName: str
    AttributeType: str


class KeySchema(BaseModel):
    AttributeName: str
    KeyType: str


class ProvisionedSchema(BaseModel):
    ReadCapacityUnits: int
    WriteCapacityUnits: int

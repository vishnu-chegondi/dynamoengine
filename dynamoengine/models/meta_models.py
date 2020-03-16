from pydantic import BaseModel, EmailStr, create_model
from dynamoengine.fields import KeySchema, AttributeSchema, ProvisionedSchema
from dynamoengine.queries import Cursor


class BaseTableModel(BaseModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_table(self):
        return (type(self).__name__)

    def save(self):
        for i, j in self.dict().items():
            if isinstance(j, str):
                self._item[i] = {'S': j}
            elif isinstance(j, int):
                self._item[i] = {'N': str(j)}
        table_name = self.get_table()
        reponse = self._cursor.client.put_item(
            TableName=table_name,
            Item=self._item
        )
        return reponse


class MetaModel():

    def __new__(cls, **kwargs):
        attr_dict = {}
        for column, value in cls.__dict__.items():
            if column[:2] != "__":
                if value.attr_type == 'S':
                    attr_dict[column] = (str, ...)
                elif value.attr_type == 'N':
                    attr_dict[column] = (int, ...)
                elif value.attr_type == 'E':
                    attr_dict[column] = (EmailStr, ...)
        TempTableModel = create_model(
            cls.__table__,
            _item={},
            _cursor=Cursor(),
            __base__=BaseTableModel,
            **attr_dict
            )
        instance = TempTableModel(**kwargs)
        return instance

    @classmethod
    def create_schema(cls):
        cls.__attribute_definition__ = []
        cls.__key_schema__ = []
        for column, value in cls.__dict__.items():
            if column[:2] != "__":
                if value.meta_schema:
                    value.meta_schema.update_name(column)
                    cls.__attribute_definition__.append(
                        AttributeSchema(**value.meta_schema.dict()).dict()
                    )
                    cls.__key_schema__.append(
                        KeySchema(**value.meta_schema.dict()).dict()
                    )
        cls.__provisioned_throughput = ProvisionedSchema(
            **dict(
                    ReadCapacityUnits=cls.__read_capacity__,
                    WriteCapacityUnits=cls.__write_capacity__
                )
            ).dict()

    @classmethod
    def create_table(cls):
        cls.create_schema()
        cursor = Cursor()
        cursor.client.create_table(
            TableName=cls.__table__,
            AttributeDefinitions=cls.__attribute_definition__,
            KeySchema=cls.__key_schema__,
            ProvisionedThroughput=cls.__provisioned_throughput
        )

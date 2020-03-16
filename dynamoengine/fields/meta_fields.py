from pydantic import create_model, BaseModel, EmailStr

from dynamoengine.fields.schemas import MetaSchema
from dynamoengine.exceptions import DynamoValueError


class BaseFieldModel(BaseModel):
    meta_schema: MetaSchema = None
    attr_type: str = None


class FactoryField():

    def __new__(cls):
        if cls.attr_type == 'S':
            CharFieldModel = create_model(
                'CharFieldModel',
                data=(str, None),
                __base__=BaseFieldModel
            )
            instance = CharFieldModel(attr_type="S")
            return instance
        elif cls.attr_type == 'N':
            IntFieldModel = create_model(
                'IntFieldModel',
                data=(int, None),
                __base__=BaseFieldModel
            )
            instance = IntFieldModel(attr_type="N")
            return instance
        elif cls.attr_type == 'E':
            EmailFieldModel = create_model(
                'EmailFieldModel',
                data=(EmailStr, None),
                __base__=BaseFieldModel
            )
            cls.attr_type = 'S'
            instance = EmailFieldModel(attr_type="E")
            return instance


class FactoryMetaSchema():

    def __new__(cls, name="Test", attr_type=None, key=None):
        data = dict(
            AttributeName=name,
            KeyType=key,
            AttributeType=attr_type
        )
        return MetaSchema(**data)


class UnicodeAttribute():

    def __new__(cls, **kwargs):
        instance = FactoryField.__new__(cls)
        if 'hash_key' in kwargs and 'range_key' in kwargs:
            raise DynamoValueError(
                message="Can not assign both hash_key and range_key",
                solution="Set column as either hash_key or range_key "
            )
        elif 'hash_key' in kwargs:
            instance.meta_schema = FactoryMetaSchema(
                attr_type=cls.attr_type,
                key='HASH'
            )
        elif 'range_key' in kwargs:
            instance.meta_schema = FactoryMetaSchema(
                attr_type=cls.attr_type,
                key='RANGE'
            )
        return instance


class CharField(UnicodeAttribute):

    def __new__(cls, **kwargs):
        cls.attr_type = 'S'
        instance = super().__new__(cls, **kwargs)
        return instance


class IntegerField(UnicodeAttribute):

    def __new__(cls, **kwargs):
        cls.attr_type = 'N'
        instance = super().__new__(cls, **kwargs)
        return instance


class EmailField(UnicodeAttribute):

    def __new__(cls, **kwargs):
        cls.attr_type = 'E'
        instance = super().__new__(cls, **kwargs)
        return instance

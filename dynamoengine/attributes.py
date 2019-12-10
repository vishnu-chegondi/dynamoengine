import boto3
from pydantic import BaseModel
from dynamoengine.metamodel import MetaKeySchema, MetaAttributeDef, MetaProvisionedThroughput
from typing import List, Dict, Set, Tuple


class KeySchema():

    def __new__(cls, name, key, attr_type):
        data = dict(
            AttributeName = name,
            KeyType = key,
            AttributeType = attr_type
        )
        instance = MetaKeySchema(**data)
        return instance


class AttributeDefinition():
    
    def __new__(cls, name, attr_type):
        data = dict(
            AttributeName = name,
            AttributeType = attr_type
        )
        instance = MetaAttributeDef(**data)
        return instance

class ProvisionedThroughput():

    def __new__(cls, read_capacity = None, write_capacity=None):
        data = dict()
        if read_capacity is not None and write_capacity is not None: 
            data = dict(
                ReadCapacityUnits = read_capacity,
                WriteCapacityUnits = write_capacity
            )
        instance = MetaProvisionedThroughput(**data)
        return instance


class UnicodeAttribute():

    hash_set = False
    range_set = False

    def __new__(cls, range_key=False, hash_key=False, attr_type=None):
        if hash_key and not cls.hash_set:
            cls.hash_set = True
            return KeySchema("TestDefault", "HASH", attr_type)
        elif range_key and not cls.range_set:
            cls.range_set = True
            return KeySchema("TestDefault", "RANGE", attr_type)
        else:
            return AttributeDefinition("TestDefault", attr_type)

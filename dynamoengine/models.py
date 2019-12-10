from pydantic import BaseModel

class Model():
    __table__ = None

    def __new__(cls):
        for i in cls.__dict__.keys():
            if isinstance(cls.__dict__[i], BaseModel):
                obj = (cls.__dict__[i])
                obj.AttributeName=i
        instance = object.__new__(cls)
        return instance

    @classmethod
    def create_table(cls):
        if cls.__table__ is not None:
            print (cls.__table__)
        else:
            pass

if __name__ == "__main__":
    mdl=Model()
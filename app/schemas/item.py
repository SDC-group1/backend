from pydantic import BaseModel

# inherit base class from BaseModel
class ItemBase(BaseModel):
    name: str

# input schema for POST requests 
class ItemCreate(ItemBase):
    pass

# output schema for responses 
class Item(ItemBase):
    id: int 

    class Config: 
        from_attributes = True
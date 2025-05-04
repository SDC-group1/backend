from pydantic import BaseModel, validator

# inherit base class from BaseModel
class BlogBase(BaseModel):
    name: str

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or v.isspace():
            raise ValueError('name must not be empty')
        return v

# input schema for POST requests 
class BlogCreate(BlogBase):
    pass

# output schema for responses 
class Blog(BlogBase):
    id: int 

    class Config: 
        from_attributes = True
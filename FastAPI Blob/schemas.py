from pydantic import BaseModel, ConfigDict, Field, EmailStr

from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=20)
    email: EmailStr = Field(max_length=50)


class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    model_config= ConfigDict(from_attributes=True)

    id:int
    image_file: str | None
    image_path: str

class UserUpdate(BaseModel):
    username: str | None = Field(default=None,min_length=1, max_length=20)
    email: EmailStr| None = Field(default= None,max_length=50)
    image_file: str | None = Field(default= None, min_length=1, max_length=200)

class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)
    



class PostCreate(PostBase):
    user_id: int #temporary

class PostUpdate(BaseModel):
    title: str = Field(default=None,min_length=1, max_length=100)
    content: str = Field(default=None,min_length=1)


#receives the attributes by the postbase and add id, date by the system not user
#from_attributes=True tell pydantic to read data from obj with attributes not just dictionaries
class PostResponse(PostBase):
    model_config= ConfigDict(from_attributes=True)

    id: int
    user_id : int
    date_posted: datetime
    author: UserResponse

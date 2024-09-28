from pydantic import BaseModel, Field, EmailStr, HttpUrl
from uuid import UUID, uuid4

from . import db

database = db.get_database('valeria_plays')


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    email: EmailStr
    given_name: str
    family_name: str
    picture: HttpUrl
    access_token: str

    @staticmethod
    def get_user(email: str):
        collection = database.get_collection('users')
        return collection.find_one({'email': email})

    def insert_user(self): 
        collection = database.get_collection('users')
        collection.insert_one({
            'email': self.email,
            'given_name': self.given_name,
            'family_name': self.family_name,
            'picture': str(self.picture),
            'access_token': self.access_token
        })
        
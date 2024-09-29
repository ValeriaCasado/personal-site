from pydantic import BaseModel, Field, EmailStr, HttpUrl
from uuid import UUID, uuid4

from . import db

database = db.get_database('valeria_plays')


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    email: EmailStr
    sub: str
    given_name: str
    family_name: str
    picture: HttpUrl
    active: bool = True
    anonymous: bool = False

    @classmethod
    def load_user(cls, email: str):
        collection = database.get_collection('users')
        user = collection.find_one({'email': email})
        if not user: return None
        return cls(**user)

    def save(self): 
        collection = database.get_collection('users')
        collection.insert_one({
            'email': self.email,
            'sub': self.sub,
            'given_name': self.given_name,
            'family_name': self.family_name,
            'picture': str(self.picture),
            'active': self.active,
            'anonymous': self.anonymous
        })
        return self
    
    # Functions needed for login manager
    def get_id(self):
        return self.email
    
    def is_anonymous(self): return self.anonymous

    def is_active(self): return self.active

    def is_authenticated(self): return True
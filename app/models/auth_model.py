from pydantic import BaseModel


class AuthModel(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True

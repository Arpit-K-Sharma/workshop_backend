from pydantic import BaseModel

class School(BaseModel):
  school_id:str
  course:str

class Teacher(BaseModel):
  name : str
  address : str
  username : str
  password : str
  phone_number : int
  profile_pic : str             #"./profile_pic"
  schools :School
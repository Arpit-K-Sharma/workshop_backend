from typing import List
from pydantic import BaseModel

class Student(BaseModel):
    student_name:str
    age:int
    phone_no:int
    address:str
    school_id:str
    course:str
    # gallery:
    videos:List[str]
    photos:List[str]




#   "_id": "4343",
#   "student_name": "Spandan Bhattarai",
#   "age": 19,
#   "phone_num": "9812443132",
#   "address": "Balkhu",
#   "school_id": "3324",
#   "course_id": ,

#   "gallery": ,
#      "videos":,
#     "photos": ,
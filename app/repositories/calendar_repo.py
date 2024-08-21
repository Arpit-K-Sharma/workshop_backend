from typing import Optional
from fastapi import HTTPException
from app.config.db_config import mongodb
from app.models.calendar_model import Calendar
from bson import DBRef, ObjectId
from app.dto.calendar_dto import CalendarDTOResponse, UpdateEventDTO

class CalendarRepo:
    
    @staticmethod
    async def create_academic_event(calendar: Calendar) -> dict:
        try:
            response = await mongodb.collections['calendar'].insert_one(calendar.dict(by_alias=True))
            return {"message": "Academic event created successfully"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid data: {str(e)}")
    
    @staticmethod
    async def get_calendar_by_year(year: int) -> Optional[Calendar]:
        try:
            calendar = await mongodb.collections['calendar'].find_one({"year": year}, {"_id": 0})
            if calendar:
                return Calendar(**calendar)
            return None
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to retrieve calendar: {str(e)}")

    @staticmethod
    async def update_academic_event(calendar: Calendar) -> dict:
        try:
            response = await mongodb.collections['calendar'].update_one({"year": calendar.year}, {"$set": calendar.dict(by_alias=True)})
            return {"message": "Academic event updated successfully"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to update calendar: {str(e)}")
        

    @staticmethod
    async def get_events_by_year(year: int, school_id :str):
        
        school_dbref = DBRef('school', ObjectId(school_id))
        
        # Fetch the document with the specific year
        document = await mongodb.collections['calendar'].find_one({"year": year})
        
        if document:
            # Filter out the specific school from the schools array
            schools = [school for school in document.get('schools', []) 
                       if school.get('school_id') == school_dbref]
            if schools:
                document['schools'] = schools
                return document
        return None
    
    @staticmethod
    async def get_events_by_month(year: int, school_id: str, month: int):
        school_dbref = DBRef('school', ObjectId(school_id))
        
        # Fetch the document with the specific year
        document = await mongodb.collections['calendar'].find_one({"year": year})
        
        if document:
            # Filter out the specific school from the schools array
            schools = [school for school in document.get('schools', []) 
                       if school.get('school_id') == school_dbref]
            if schools:
                # Further filter months for the specific month
                for school in schools:
                    school['months'] = [m for m in school.get('months', []) if m.get('month') == month]
                document['schools'] = schools
                return document
        return None
    
    @staticmethod
    async def get_events_by_date(year: int, school_id: str, month: int, date: int):
        school_dbref = DBRef('school', ObjectId(school_id))
        
        # Fetch the document with the specific year
        document = await mongodb.collections['calendar'].find_one({"year": year})
        
        if document:
            # Filter out the specific school from the schools array
            schools = [school for school in document.get('schools', []) 
                       if school.get('school_id') == school_dbref]
            if schools:
                # Further filter months for the specific month
                for school in schools:
                    school['months'] = [
                        m for m in school.get('months', []) 
                        if m.get('month') == month
                    ]
                    # Filter days for the specific date
                    for month in school['months']:
                        month['days'] = [
                            d for d in month.get('days', []) 
                            if d.get('day') == date
                        ]
                document['schools'] = schools
                return document
        return None


    @staticmethod
    async def update_events(year: int, school_id: str, month: int, date: int,eventID: str,updateData : UpdateEventDTO):
        school_dbref = DBRef('school', ObjectId(school_id))
        event_id = ObjectId(eventID)
        result = await mongodb.collections['calendar'].update_one(
            {
                "year": year,
                "schools.school_id": school_dbref,
                "schools.months.month": month,
                "schools.months.days.day": date,
                "schools.months.days.events._id": event_id
            },
            {
                "$set": {
                    "schools.$[school].months.$[month].days.$[day].events.$[event].event_name": updateData.event_name,
                    "schools.$[school].months.$[month].days.$[day].events.$[event].event_description": updateData.event_description
                }
            },
            array_filters=[
                {"school.school_id": school_dbref},
                {"month.month": month},
                {"day.day": date},
                {"event._id": event_id}
                # {"event.event_name": {"$exists": True}}
            ]
        )
        # print(result)
        # print(f"Matched Count: {result.matched_count}")
        # print(f"Modified Count: {result.modified_count}")
        return result.modified_count > 0
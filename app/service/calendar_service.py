from typing import List
from fastapi import HTTPException
from app.config.logger_config import get_logger
from app.dto.calendar_dto import CalendarDTO,CalendarDTOResponse, SchoolEventsDTOResponse, MonthDTOResponse, DayDTOResponse, EventTitleDTOResponse, UpdateEventDTO
from app.repositories.calendar_repo import CalendarRepo
from app.models.calendar_model import Calendar, Day, Month, SchoolEvents, EventTitle
from bson import DBRef, ObjectId

logger = get_logger()

class CalendarService:
    # @staticmethod
    # async def create_academic_event(calendar_dto: CalendarDTO):
    #     try:
    #         # Convert DTOs to model instances
    #         events = [
    #             EventTitle(
    #                 event_name=event.event_name,
    #                 event_description=event.event_description
    #             ) for event in calendar_dto.schools[0].months[0].days[0].events
    #         ]

    #         days = [
    #             Day(
    #                 day=calendar_dto.schools[0].months[0].days[0].day,
    #                 events=events
    #             )
    #         ]

    #         months = [
    #             Month(
    #                 month=calendar_dto.schools[0].months[0].month,
    #                 days=days
    #             )
    #         ]

    #         school_event = SchoolEvents(
    #             school_id=calendar_dto.schools[0].school_id,
    #             months=months  # Directly use the list of Month objects
    #         )

    #         calendar = Calendar(
    #             year=calendar_dto.year,
    #             schools=[school_event]
    #         )

    #         # Check if the year exists
    #         existing_calendar = await CalendarRepo.get_calendar_by_year(calendar.year)
    #         if existing_calendar:
    #             for school in existing_calendar.schools:
    #                 if school.school_id == calendar.schools[0].school_id:
    #                     for month in school.months:
    #                         if month.month == calendar.schools[0].months[0].month:
    #                             for day in month.days:
    #                                 if day.day == calendar.schools[0].months[0].days[0].day:
    #                                     # Update existing day's events
    #                                     day.events.extend(events)
    #                                     break
    #                             else:
    #                                 # Add new day if it doesn't exist
    #                                 month.days.append(calendar.schools[0].months[0].days[0])
    #                             break
    #                     else:
    #                         # Add new month if it doesn't exist
    #                         school.months.append(calendar.schools[0].months[0])
    #                     break
    #             else:
    #                 # Add new school if it doesn't exist
    #                 existing_calendar.schools.append(calendar.schools[0])
                
    #             await CalendarRepo.update_academic_event(existing_calendar)
    #         else:
    #             # If year doesn't exist, create new calendar entry
    #             await CalendarRepo.create_academic_event(calendar)

    #         return {"message": "Event added successfully to the calendar"}
        
    #     except Exception as e:
    #         logger.error(f"Failed to create calendar: {str(e)}")
    #         raise HTTPException(status_code=400, detail=f"Failed to create calendar: {str(e)}")
        

    @staticmethod
    async def create_academic_event(calendar_dto: CalendarDTO):
        try:
            # Create a calendar object
            calendar = Calendar(
                year=calendar_dto.year,
                schools=[]  # Initialize an empty list for schools
            )

            # Iterate through each school in the DTO
            for school_dto in calendar_dto.schools:
                # Convert months and their days and events
                months = []
                for month_dto in school_dto.months:
                    days = []
                    for day_dto in month_dto.days:
                        events = [
                            EventTitle(
                                event_name=event.event_name,
                                event_description=event.event_description
                            ) for event in day_dto.events
                        ]
                        days.append(Day(
                            day=day_dto.day,
                            events=events
                        ))
                    months.append(Month(
                        month=month_dto.month,
                        days=days
                    ))

                school_event = SchoolEvents(
                    school_id=school_dto.school_id,
                    months=months
                )

                # Add the school event to the calendar
                calendar.schools.append(school_event)

            # Check if the year exists
            existing_calendar = await CalendarRepo.get_calendar_by_year(calendar.year)
            if existing_calendar:
                for school_event in calendar.schools:
                    # Check for existing school in the calendar
                    for existing_school in existing_calendar.schools:
                        if existing_school.school_id == school_event.school_id:
                            # Handle existing months and days
                            for month in school_event.months:
                                for existing_month in existing_school.months:
                                    if existing_month.month == month.month:
                                        for day in month.days:
                                            for existing_day in existing_month.days:
                                                if existing_day.day == day.day:
                                                    # Update existing day's events
                                                    existing_day.events.extend(day.events)
                                                    break
                                            else:
                                                # Add new day if it doesn't exist
                                                existing_month.days.append(day)
                                        break
                                else:
                                    # Add new month if it doesn't exist
                                    existing_school.months.append(month)
                            break
                    else:
                        # Add new school if it doesn't exist
                        existing_calendar.schools.append(school_event)

                await CalendarRepo.update_academic_event(existing_calendar)
            else:
                # If year doesn't exist, create new calendar entry
                await CalendarRepo.create_academic_event(calendar)

            return {"message": "Events added successfully to the calendar"}
        
        except Exception as e:
            logger.error(f"Failed to create calendar: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Failed to create calendar: {str(e)}")

    @staticmethod
    async def get_events_by_year(year : int, school_id : str):

        document = await CalendarRepo.get_events_by_year(year, school_id)
        if document:
            school_events = []
            for school in document.get('schools', []):
                # Convert school_id from DBRef to string
                school_id_str = str(school.get('school_id').id) if isinstance(school.get('school_id'), DBRef) else school.get('school_id')
                
                months = []
                for month in school.get('months', []):
                    days = []
                    for day in month.get('days', []):
                        events = [EventTitleDTOResponse(
                            id = event.get('_id'),
                            event_name=event.get('event_name'),
                            event_description=event.get('event_description')
                        ) for event in day.get('events', [])]
                        days.append(DayDTOResponse(
                            day=day.get('day'),
                            events=events
                        ))
                    months.append(MonthDTOResponse(
                        month=month.get('month'),
                        days=days
                    ))
                
                school_events.append(SchoolEventsDTOResponse(
                    school_id=school_id_str,
                    events=months
                ))
            
            response = CalendarDTOResponse(
                year=document['year'],
                schools=school_events
            )
            return response
        return None
    

    @staticmethod
    async def get_events_by_month(year :int, school_id: str, month: int):
        document = await CalendarRepo.get_events_by_month(year, school_id, month)
        if document:
            school_events = []
            for school in document.get('schools', []):
                # Convert school_id from DBRef to string
                school_id_str = str(school.get('school_id').id) if isinstance(school.get('school_id'), DBRef) else school.get('school_id')
                
                months = []
                for month_data in school.get('months', []):
                    days = []
                    for day in month_data.get('days', []):
                        events = [EventTitleDTOResponse(
                             id = event.get('_id'),
                            event_name=event.get('event_name'),
                            event_description=event.get('event_description')
                        ) for event in day.get('events', [])]
                        days.append(DayDTOResponse(
                            day=day.get('day'),
                            events=events
                        ))
                    months.append(MonthDTOResponse(
                        month=month_data.get('month'),
                        days=days
                    ))
                
                school_events.append(SchoolEventsDTOResponse(
                    school_id=school_id_str,
                    events=months
                ))
            
            response = CalendarDTOResponse(
                year=document['year'],
                schools=school_events
            )
            return response
        return None
    
    @staticmethod
    async def get_events_by_date(year :int, school_id: str, month: int, date: int):
        document = await CalendarRepo.get_events_by_date(year, school_id, month, date)
        if document:
            school_events = []
            for school in document.get('schools', []):
                # Convert school_id from DBRef to string
                school_id_str = str(school.get('school_id').id) if isinstance(school.get('school_id'), DBRef) else school.get('school_id')
                
                months = []
                for month_data in school.get('months', []):
                    days = []
                    for day in month_data.get('days', []):
                        events = [EventTitleDTOResponse(
                             id = event.get('_id'),
                            event_name=event.get('event_name'),
                            event_description=event.get('event_description')
                        ) for event in day.get('events', [])]
                        days.append(DayDTOResponse(
                            day=day.get('day'),
                            events=events
                        ))
                    months.append(MonthDTOResponse(
                        month=month_data.get('month'),
                        days=days
                    ))
                
                school_events.append(SchoolEventsDTOResponse(
                    school_id=school_id_str,
                    events=months
                ))
            
            response = CalendarDTOResponse(
                year=document['year'],
                schools=school_events
            )
            return response
        return None
    
    @staticmethod
    async def update_events(year: int, school_id: str, month: int, date: int,eventID: str ,updateDTO : UpdateEventDTO):
        document = await CalendarRepo.get_events_by_date(year, school_id, month, date)
        # print(document)
        if document:
            updated = await CalendarRepo.update_events(
            year, school_id, month, date, eventID, updateDTO )

            # print(updated)
        return updated

from fastapi import APIRouter, HTTPException
from typing import List
from .models import Event, Joiner
from .file_storage import EventFileManager
from .event_analyzer import EventAnalyzer
router = APIRouter()


@router.get("/events", response_model=List[Event])
async def get_all_events():
    events = EventFileManager()
    return events.read_events_from_file()


@router.get("/events/filter", response_model=List[Event])
async def get_events_by_filter(date: str = None, organizer: str = None, status: str = None, event_type: str = None):
    events = EventFileManager()
    list = events.read_events_from_file()

    res = []

    for e in list:
        if e.date == date or e.type == event_type or e.organizer.name == organizer or e.status == status:
            res.append(e)
    return res


@router.get("/events/{event_id}", response_model=Event)
async def get_event_by_id(event_id: int):
    events = EventFileManager()

    list = events.read_events_from_file()

    for e in list:
        if e.id == event_id:
            return e

    raise HTTPException(status_code=404, detail="Event not found!")


@router.post("/events", response_model=Event)
async def create_event(event: Event):
    events = EventFileManager()

    list = events.read_events_from_file()
    for e in list:
        if e.id == event.id:
            raise HTTPException(status_code=400, detail="Event ID already exists!")
    list.append(event)

    events.write_events_to_file(list)


@router.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: int, event: Event):
    events = EventFileManager()
    list = events.read_events_from_file()

    for i in range(len(list)):
        e = list[i]
        if event_id == e.id:
            list[i] = event
            return
    raise HTTPException(status_code=404, detail="Event not found!")


@router.delete("/events/{event_id}")
async def delete_event(event_id: int):
    events = EventFileManager()
    list = events.read_events_from_file()

    for i in range(len(list)):
        e = list[i]
        if e.id == event_id:
            list.remove(e)
            return
    raise HTTPException(status_code=404, detail="Event not found")


@router.get("/events/joiners/multiple-meetings", response_model=List[Joiner])
async def get_joiners_multiple_meetings():
    events = EventFileManager()
    analyzer = EventAnalyzer()

    list = events.read_events_from_file()
    res = analyzer.get_joiners_multiple_meetings_method(list)

    return res

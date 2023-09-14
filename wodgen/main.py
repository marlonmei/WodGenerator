import csv
import random

from sqlalchemy import and_
from sqlalchemy.orm import Session
from fastapi import FastAPI, Request, Depends, UploadFile, HTTPException
from fastapi.templating import Jinja2Templates

from database import engine, get_database_session
from pydantic import BaseModel

from models import Workout, Base
from type import WorkoutType

from data.verification import verify_workout_type
from constants import TIME_MAPPING
from config import TEMPLATES_DIRECTORY, CSV_ENCODING_UPLOAD


app = FastAPI()
Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory=TEMPLATES_DIRECTORY)


class WorkoutRequest(BaseModel):
    name: str


class GenerateRequest(BaseModel):
    workout_type: WorkoutType
    time: float


@app.get("/")
def home(request: Request):
    """

    Homepage / Dashboard to display workouts

    """
    return templates.TemplateResponse(
        "home.html",
        {"request": request}
    )


@app.get("/GenerateWorkout")
async def generate_workout(
        request: GenerateRequest = Depends(),
        session: Session = Depends(get_database_session)
):
    """
    Route for generating a workout from the database

    """

    workout_type = request.workout_type
    time = request.time
    time_range = TIME_MAPPING[time]

    filters = [
        Workout.type == workout_type.value,
        Workout.time.in_(time_range)
    ]

    all_workouts = session.query(Workout).filter(and_(*filters)).all()
    workout = random.choice(all_workouts)

    return {
        "code": "success",
        "workout": workout
    }


@app.post("/CreateWorkout")
def create_workout(
        request: WorkoutRequest,
        session: Session = Depends(get_database_session)
):
    """
    Endpoint for creating a workout

    """
    print(request)
    workout = Workout()
    workout.name = request.name

    session.add(workout)
    session.commit()
    return {
        "code": "success",
        "msg": "workout created"
    }


@app.post('/UploadWorkout')
async def upload_workout_csv(
        file: UploadFile,
        session: Session = Depends(get_database_session)
):
    try:
        csv_data = await file.read()
        csv_data = csv_data.decode(CSV_ENCODING_UPLOAD).splitlines()
        csv_reader = csv.DictReader(csv_data)
        for row in csv_reader:
            name = row['name']
            time = row['time']
            workout_type = row['workout_type']
            description = row['description']

            workout_information = str(name) + str(description)
            if workout_type is None and workout_information is not None:
                workout_type = verify_workout_type(workout_information)
            elif workout_type is not None:
                workout_type = WorkoutType(workout_type)
            else:
                workout_type = None

            workout = Workout(
                name=name,
                time=time,
                type=workout_type,
                description=description,
            )
            session.add(workout)

        session.commit()

        return {"code": "success", "msg": "CSV data imported successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

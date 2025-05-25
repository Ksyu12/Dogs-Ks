from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="FastAPI",
    version="0.1.0",  
)

class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"

class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType

class Timestamp(BaseModel):
    id: int
    timestamp: int

dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


# 2. Реализован путь /
@app.get("/", summary="Get a welcome message")
def read_root():
    return {"message": "Welcome to the Veterinary Clinic API!"}


# 3. Реализован путь /post
@app.get("/post", response_model=list[Timestamp], summary="Get all posts")
def get_posts():
    return post_db


# 4. Реализована запись собак
@app.post("/dogs", response_model=Dog, status_code=201, summary="Create a new dog")
def create_dog(dog: Dog):
    if dog.pk in dogs_db:
        raise HTTPException(status_code=400, detail="Dog with this pk already exists")
    dogs_db[dog.pk] = dog
    return dog


# 5. Реализовано получение списка собак и 7. Реализовано получение собак по типу
@app.get("/dogs", response_model=list[Dog], summary="Get all dogs or dogs by type")
def get_dogs(kind: DogType | None = None):
    if kind:
        return [dog for dog in dogs_db.values() if dog.kind == kind]
    return list(dogs_db.values())


# 6. Реализовано получение собаки по id
@app.get("/dogs/{pk}", response_model=Dog, summary="Get a dog by ID")
def get_dog_by_pk(pk: int):
    if pk not in dogs_db:
        raise HTTPException(status_code=404, detail="Dog not found")
    return dogs_db[pk]


# 8. Реализовано обновление собаки по id
@app.put("/dogs/{pk}", response_model=Dog, summary="Update a dog by ID")
def update_dog(pk: int, dog: Dog):
    if pk not in dogs_db:
        raise HTTPException(status_code=404, detail="Dog not found")
    if dog.pk != pk:
        raise HTTPException(status_code=400, detail="PK in request body must match PK in path")
    dogs_db[pk] = dog
    return dog

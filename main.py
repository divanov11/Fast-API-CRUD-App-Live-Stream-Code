from fastapi import Body, Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import models
import schemas
from database import Base, SessionLocal, engine

Base.metadata.create_all(engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


app = FastAPI()

fakeDatabase = {
    1: {'task': 'Clean car'},
    2: {'task': 'Write blog'},
    3: {'task': 'Start stream'},
}

# Different way using "status"


@app.get("/", status_code=status.HTTP_200_OK)
def getItems(session: Session = Depends(get_session)):
    return session.query(models.Item).all()


@app.get("/{id}", status_code=200)
def getItem(id: int, session: Session = Depends(get_session)):
    return session.query(models.Item).get(id)

# option #1
# @app.post("/")
# def addItem(task:str):
#     newId = len(fakeDatabase.keys()) + 1
#     fakeDatabase[newId] = {"task":task}
#     return fakeDatabase

# Option #2


@app.post("/", status_code=201)
def addItem(item: schemas.Item, session: Session = Depends(get_session)):
    item = models.Item(task=item.task)
    session.add(item)
    session.commit()
    session.refresh(item)

    return item

# Option #3
# @app.post("/")
# def addItem(body = Body()):
#     newId = len(fakeDatabase.keys()) + 1
#     fakeDatabase[newId] = {"task":body['task']}
#     return fakeDatabase


@app.put("/{id}", status_code=200)
def updateItem(id: int, item: schemas.Item, session: Session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    itemObject.task = item.task
    session.commit()
    return itemObject


@app.delete("/{id}")
def deleteItem(id: int, session: Session = Depends(get_session)):
    try:
        itemObject = session.query(models.Item).get(id)
        session.delete(itemObject)
        session.commit()
        session.close()
    except Exception:
        # You could also use "HTTPException"
        return JSONResponse(
            status_code=404,
            content={
                "message": "Item Not Found"},
        )

from fastapi import FastAPI , Body , Depends
import schemas
import models

from database import Base , engine , SessionLocal
from sqlalchemy.orm import Session

Base.metadata.create_all(engine)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

app = FastAPI()

fakedatabase = {
    1:{'task':'clean car'},
    2:{'task':'write blog'},
    3:{'task':'start stream,'}
}
@app.get("/")
def getItems(session: Session = Depends(get_session)):
    items = session.query(models.Item).all()
    return items

@app.get("/{id}")
def getItem(id:int,session: Session = Depends(get_session)):
    item = session.query(models.Item).get(id)
    return item

#option 1
# @app.post("/")
# def addItem(task:str):
#     newId = len(fakedatabase.keys()) + 1
#     fakedatabase[newId] = {'task':task}
#     return fakedatabase

#option 2
@app.post("/")
def addItem(item:schemas.Item , session: Session = Depends(get_session)):
    item = models.Item(task=item.task)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


    # newId = len(fakedatabase.keys()) + 1
    # fakedatabase[newId] = {'task':item.task}
    # return fakedatabase

#option 3
#@app.post("/")
# def addItem(body = Body()):
#     newId = len(fakedatabase.keys()) + 1
#     fakedatabase[newId] = {'task':body['task']}
#     return fakedatabase

@app.put("/{id}")
def updateItem(id:int,item:schemas.Item ,session: Session = Depends(get_session)):
    itemobject = session.query(models.Item).get(id)
    itemobject.task = item.task
    session.commit()
    return itemobject

    # fakedatabase[id]['task'] = item.task
    # return fakedatabase

@app.delete("/{id}")
def deleteItem(id:int,session: Session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    session.delete(itemObject)
    session.commit()
    return {"message":"Item deleted"}

    # del fakedatabase[id]
    # return fakedatabase
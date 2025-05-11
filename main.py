from fastapi import FastAPI, HTTPException, Depends
from typing import List

import models, database  
from sqlalchemy.orm import Session

app = FastAPI()

# Dependency to get the database session
def get_db(db: Session = Depends(database.get_db)):
    return db

@app.post("/tasks/", response_model=models.Task, status_code=201)
async def create_task(task: models.TaskCreate, db: Session = Depends(get_db)):
    db_task = database.TaskDB(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks/", response_model=List[models.Task])
async def read_tasks(db: Session = Depends(get_db)):
    tasks = db.query(database.TaskDB).all()
    return tasks

@app.get("/tasks/{task_id}", response_model=models.Task)
async def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(database.TaskDB).filter(database.TaskDB.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.put("/tasks/{task_id}", response_model=models.Task)
async def update_task(task_id: int, updated_task: models.TaskCreate, db: Session = Depends(get_db)):
    db_task = db.query(database.TaskDB).filter(database.TaskDB.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in updated_task.model_dump().items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(database.TaskDB).filter(database.TaskDB.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return
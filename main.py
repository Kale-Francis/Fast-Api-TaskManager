from fastapi import FastAPI, HTTPException
from typing import List

from models import Task, TaskCreate

app = FastAPI()

# A simple in memory task storage
tasks = []
task_id_counter = 0

@app.post("/tasks/", response_model=Task, status_code=201) # Defines a POST request handeler for the task endpoint used for creating new tasks"""
async def create_task(task: TaskCreate):
	global task_id_counter
	task_id_counter += 1
	new_task = Task(id=task_id_counter, **task.model_dump())
	tasks.append(new_task)
	return new_task

@app.get("/tasks/", response_model=List[Task]) # Defines GET request for the endpoint used for retriving all tasks
async def read_tasks():
	return tasks

@app.get("/tasks/{task_id}", response_model=Task) # Defines GET request for the endpoint used for retriving all tasks
async def read_task(task_id: int):
	for task in tasks:
		return task
	raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}", response_model=Task) # Defines PUT request for updating an exsting task
async def update_task(task_id: int, updated_task: TaskCreate):
	for index, task in enumerate(tasks):
		if task.id == task_id:
			tasks[index] = Task(id=task_id, **updated_task.model_dump())
			return tasks[index]
	raise HTTPException(status_code=404, detail="Task not Found")

@app.delete("/tasks/{task_id}", status_code=204) # Defines DELETE request for deleting a task
async def delete_task(task_id: int):
	for index, task in enumerate(tasks):
		del tasks[index]
		return
	raise HTTPException(status_code=404, detail="Task not Found")

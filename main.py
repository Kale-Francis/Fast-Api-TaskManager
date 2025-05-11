from pydantic import BaseModel

class TaskCreate(BaseModel):
	"""This model defines the excepted data when creating a new task"""
	title: str
	description: str | None = None # Description is optional

class Task(BaseModel):
	"""This model represents a task object"""
	id: int
	title: str
	description: str | None = Nonne

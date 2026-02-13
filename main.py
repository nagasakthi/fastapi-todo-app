from fastapi import FastAPI ,Request
import models
from database import engine
from routers import auth , todos , admin , users
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app =FastAPI()

models.Base.metadata.create_all(bind=engine)# todos.db will be created automatically
templates = Jinja2Templates(directory="templates")  # Todo/templates

app.mount("/static", StaticFiles(directory="static"), name="static")  #Todo/static


@app.get("/")
def test(request: Request):
    return templates.TemplateResponse("register.html",context={"request":request})

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)




################################################################################





# from fastapi import FastAPI, Request, status
# # from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles
# from starlette.responses import RedirectResponse
#
# import models
# from database import engine
# from routers import auth, todos, admin, users
#
# # from Todo import models
#
# app =FastAPI()
#
# app.mount("/static", StaticFiles(directory="static"), name="static")
# models.Base.metadata.create_all(bind=engine)   # todos.db will be created automatically
# # templates = Jinja2Templates(directory="templates")
#
#
# @app.get("/")
# def test(request: Request):
#     # return templates.TemplateResponse("home.html", {"request": request})
#     return RedirectResponse("/todos/todo-page", status_code=status.HTTP_302_FOUND)
# app.include_router(auth.router)
# app.include_router(todos.router)
# app.include_router(admin.router)
# app.include_router(users.router)





# # Dependency for DB session:
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
# db_dependency = Annotated[Session, Depends(get_db)]
#
# class TodoRequest(BaseModel):
#     title: str = Field(min_length=3)
#     description: str = Field(min_length=3, max_length=100)
#     priority: int = Field(default=1, gt=0, lt=6)
#     complete: bool
#
#
# @app.get("/")
# async def read_all(db: db_dependency):
#     return db.query(models.Todos).all()
#
#
# # @app.get("/todo/todos/{todo_id}", status_code=status.HTTP_200_OK)
# # async def read_all(db: db_dependency, todo_id: int = Path(gt=0)):
# #     todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
# #     if todo_model is None:
# #         raise HTTPException(status_code=404, detail = "Todo Not Found")
# #     return todo_model
#
# @app.get("/todo/todos/{todo_id}")
# async def read_by_id(db: db_dependency, todo_id: int):
#     todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
#     if todo_model is None:
#         raise HTTPException(status_code=404, detail = "Todo Not Found")
#     return todo_model
#
# # @app.post("/todo/", status_code=status.HTTP_201_CREATED)
# # def create(todo_request : TodoRequest, db: db_dependency):
# #     new_todo = Todos(**todo_request.model_dump())
# #     db.add(new_todo)
# #     db.commit()
# #     db.refresh(new_todo)
# #     return new_todo
#
# @app.post("/todo/")
# def create(todo_request : TodoRequest, db: db_dependency):
#     new_todo = Todos(**todo_request.model_dump())
#     db.add(new_todo)
#     db.commit()
#     db.refresh(new_todo)
#     return new_todo
#
# @app.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
# # def update(todo_id: int = Path(gt=0) , todo_request : TodoRequest, db: db_dependency):   #L# non-default parameter follows default parameter
# def update(todo_request: TodoRequest, db: db_dependency, todo_id: int = Path(gt=0)):
#     todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
#     if todo_model is None:
#         raise HTTPException(status_code=404, detail = "Todo Not Found")
#     todo_model.title = todo_request.title
#     todo_model.description = todo_request.description
#     todo_model.priority = todo_request.priority
#     todo_model.complete = todo_request.complete
#     db.add(todo_model)
#     db.commit()
#     db.refresh(todo_model)
#     return todo_model
#
#
# @app.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
# # def delete(todo_request: TodoRequest, db: db_dependency,todo_id: int = Path(gt=0)):     #L# Request body is not required here as we are deleting
# def delete(db: db_dependency,todo_id: int = Path(gt=0)):
#     todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
#     if todo_model is not None:
#         db.query(Todos).filter(Todos.id == todo_id).delete()
#         db.commit()
#     # raise HTTPException(status_code=404, detail="Todo Not Found")
























# from contextlib import redirect_stderr
# from fastapi import Depends, HTTPException, Path, APIRouter,Request,status
# from typing import Annotated
# from pydantic import BaseModel, Field
# from sqlalchemy.orm import Session
# from starlette import status
# import models
# from database import SessionLocal
# from models import Todo
# from .auth import get_current_user
# from starlette.responses import RedirectResponse
# from fastapi.templating import Jinja2Templates
#
# templates = Jinja2Templates(directory="templates")
#
# router = APIRouter(
#     prefix="/todos",
#     tags=["todos"]
# )
#
# # Dependency for DB session:
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
# db_dependency = Annotated[Session, Depends(get_db)]
# user_dependency = Annotated[dict, Depends(get_current_user)]
#
# class TodoRequest(BaseModel):
#     title: str = Field(min_length=3)
#     description: str = Field(min_length=3, max_length=100)
#     priority: int = Field(default=1, gt=0, lt=6)
#     complete: bool
#
# def redirect_to_login():
#     redirect_response = RedirectResponse(url="/auth/login_page",status_code=status.HTTP_302_FOUND)
#     redirect_response.delete_cookie(key="access_token")
#     return redirect_response
#
# ###### PAGES #####
# @router.get("/todo-page")
# async def render_todo_page(request: Request,db:db_dependency=Depends(get_db)):
#     try:
#         user = await get_current_user(request.cookies.get("access_token"))
#         if user is None:
#             return redirect_to_login()
#         todos= db.query(Todo).filter(Todo.owner_id == user.get("id")).all()
#         return templates.TemplateResponse("todo.html", {"request": request, "todos": todos, "user": user})
#     except :
#         return redirect_to_login()
#
#
# #### ENDPOINTS ########
#
#
# @router.get("/")
# async def read_all(db: db_dependency,user: user_dependency):
#     # return db.query(models.Todo).all()
#     return db.query(models.Todo).filter(Todo.owner_id == user.get('id')).all()
#
#
# # @app.get("/todo/todos/{todo_id}", status_code=status.HTTP_200_OK)
# # async def read_all(db: db_dependency, todo_id: int = Path(gt=0)):
# #     todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
# #     if todo_model is None:
# #         raise HTTPException(status_code=404, detail = "Todo Not Found")
# #     return todo_model
#
# @router.get("/{todo_id}")
# async def read_by_id(db: db_dependency, todo_id: int, user: user_dependency):
#     # todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
#     todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user.get('id')).first()
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
# @router.post("/")
# def create(todo_request : TodoRequest, db: db_dependency,user: user_dependency):
#     if user is None:
#         raise HTTPException(status_code=401, detail = "Authentication Failed")
#     # new_todo = Todo(**todo_request.model_dump())
#     new_todo = Todo(**todo_request.model_dump(),owner_id = user.get('id'))
#     db.add(new_todo)
#     db.commit()
#     db.refresh(new_todo)
#     return new_todo
#
# @router.put("/{todo_id}") #status_code=status.HTTP_200_OK)
# # def update(todo_id: int = Path(gt=0) , todo_request : TodoRequest, db: db_dependency):   #L# non-default parameter follows default parameter
# def update(todo_request: TodoRequest, db: db_dependency,user : user_dependency, todo_id: int = Path(gt=0)):
#     # todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
#     todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user.get('id')).first()
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
# @router.delete("/{todo_id}") #status_code=status.HTTP_200_OK)
# # def delete(todo_request: TodoRequest, db: db_dependency,todo_id: int = Path(gt=0)):     #L# Request body is not required here as we are deleting
# def delete(db: db_dependency,user : user_dependency,todo_id: int = Path(gt=0)):
#     todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user.get('id')).first()
#     if todo_model is not None:
#         db.query(Todo).filter(Todo.id == todo_id).delete()
#         db.commit()
#         return {"message": "Deleted successfully", "app": todo_model}
#     raise HTTPException(status_code=404, detail="Todo Not Found")
#

from typing import Annotated
from fastapi import  Depends, HTTPException, Path, APIRouter, Request , Form
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
import models
from database import SessionLocal
from .auth import get_current_user
from models import Todo
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router =APIRouter(
    prefix="/todos",
    tags=["todos"]
)

# Dependency for DB session:
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(default=1, gt=0, lt=6)
    complete: bool

def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response


### Pages ###

@router.get("/todo-page")
async def todo_page(request: Request, db: db_dependency):
    user = await get_current_user(request.cookies.get("access_token"))
    if not user:
        return redirect_to_login()

    todos = db.query(Todo).filter(
        Todo.owner_id == user["id"]
    ).all()

    return templates.TemplateResponse(
        "todo.html",
        {"request": request, "todos": todos, "user": user}
    )


@router.get("/add-todo-page")
async def add_todo_page(request: Request):
    user = await get_current_user(request.cookies.get("access_token"))
    if not user:
        return redirect_to_login()

    return templates.TemplateResponse(
        "add-todo.html",
        {"request": request, "user": user}
    )


# ---------------- ADD TODO ----------------

@router.post("/add-todo")
async def add_todo(
    request: Request,
    db: db_dependency,
    title: str = Form(...),
    description: str = Form(...),
    priority: int = Form(...),

):
    user = await get_current_user(request.cookies.get("access_token"))
    if not user:
        return redirect_to_login()

    todo = Todo(
        title=title,
        description=description,
        priority=priority,
        complete=False,
        owner_id=user["id"]
    )

    db.add(todo)
    db.commit()

    return RedirectResponse(
        url="/todos/todo-page",
        status_code=status.HTTP_303_SEE_OTHER
    )


# ---------------- EDIT TODO ----------------

@router.get("/edit-todo-page/{todo_id}")
async def edit_todo_page(
    request: Request,
    todo_id: int,
    db: db_dependency
):
    user = await get_current_user(request.cookies.get("access_token"))
    if not user:
        return redirect_to_login()

    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.owner_id == user["id"]
    ).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return templates.TemplateResponse(
        "edit-todo.html",
        {"request": request, "todo": todo, "user": user}
    )


@router.post("/edit-todo/{todo_id}")
async def update_todo(
    request: Request,
    db: db_dependency,
    todo_id: int,
    title: str = Form(...),
    description: str = Form(...),
    priority: int = Form(...),
    ):
    user = await get_current_user(request.cookies.get("access_token"))
    if not user:
        return redirect_to_login()

    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.owner_id == user["id"]
    ).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo.title = title
    todo.description = description
    todo.priority = priority

    db.commit()

    return RedirectResponse(
        url="/todos/todo-page",
        status_code=status.HTTP_303_SEE_OTHER
    )



### Endpoints ###
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return (db.query(Todo)
            .filter(Todo.owner_id==user.get("id"))
            .all())

@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_by_id(user: user_dependency, db: db_dependency, todo_id: int):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    todo_model = (db.query(Todo)
                  .filter(Todo.id == todo_id)
                  .filter(Todo.owner_id == user.get("id"))
                  .first())
    if todo_model is None:
        raise HTTPException(status_code=404, detail = "Todo Not Found")
    return todo_model

@router.post("/", status_code=status.HTTP_201_CREATED)
def create(todo_request : TodoRequest, db: db_dependency, user : user_dependency ):
    new_todo = Todo(**todo_request.model_dump())
    if user is None:
        raise HTTPException(status_code=401, detail = "Authentication Failed")
    new_todo = Todo(**todo_request.model_dump(), owner_id = user.get("id"))
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
# def update(todo_id: int = Path(gt=0) , todo_request : TodoRequest, db: db_dependency):   #L# non-default parameter follows default parameter
def update( todo_request: TodoRequest, db: db_dependency, user:user_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail = "Authentication Failed")
    todo_model = (db.query(Todo)
                  .filter(Todo.id == todo_id)
                  .filter(Todo.owner_id == user["id"])
                  .first())

    if todo_model is None:
        raise HTTPException(status_code=404, detail = "Todo Not Found")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)

    return

# @router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete(user:user_dependency, db: db_dependency,todo_id: int = Path(gt=0)):
#     if user is None:
#         raise HTTPException(status_code=401, detail = "Authentication Failed")
#     todo_model = (db.query(Todo)
#                   .filter(Todo.id == todo_id)
#                   .filter(Todo.owner_id == user["id"])
#                   .first())
#     if todo_model is not None:
#         (db.query(Todo)
#          .filter(Todo.id == todo_id)
#          .filter(Todo.owner_id == user["id"]) # If this line is not given, then this deletes ANY todo with matching ID, even if not owned by the current user.
#          .delete())
#         db.commit()
#     return {"message": "Todo deleted successfully"}
    # raise HTTPException(status_code=404, detail="Todo Not Found")
@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    request: Request,
    todo_id: int = Path(gt=0),
    db: Session = Depends(get_db)
):
    user = await get_current_user(request.cookies.get("access_token"))
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.owner_id == user["id"]
    ).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo Not Found")

    db.delete(todo)
    db.commit()

# @router.get("/")
# async def read_all(db: db_dependency):
#     return db.query(Todos).all()

# @app.get("/todo/todos/{todo_id}", status_code=status.HTTP_200_OK)
# async def read_all(db: db_dependency, todo_id: int = Path(gt=0)):
#     todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
#     if todo_model is None:
#         raise HTTPException(status_code=404, detail = "Todo Not Found")
#     return todo_model

# @router.get("/{todo_id}")
# async def read_by_id(db: db_dependency, todo_id: int):
#     todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
#     if todo_model is None:
#         raise HTTPException(status_code=404, detail = "Todo Not Found")
#     return todo_model

# @app.post("/todo/", status_code=status.HTTP_201_CREATED)
# def create(todo_request : TodoRequest, db: db_dependency):
#     new_todo = Todos(**todo_request.model_dump())
#     db.add(new_todo)
#     db.commit()
#     db.refresh(new_todo)
#     return new_todo

# @router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
# # def delete(todo_request: TodoRequest, db: db_dependency,todo_id: int = Path(gt=0)):     #L# Request body is not required here as we are deleting
# def delete(db: db_dependency,todo_id: int = Path(gt=0)):
#     todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
#     if todo_model is not None:
#         db.query(Todos).filter(Todos.id == todo_id).delete()
#         db.commit()
#     # raise HTTPException(status_code=404, detail="Todo Not Found")









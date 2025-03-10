from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models import Author, Book
from database import engine
import models
app = FastAPI()

models.Base.metadata.create_all(bind=engine)


class AuthorCreate(BaseModel):
    author_name: str

class BookCreate(BaseModel):
    book_name: str
    book_description: str
    author_id: int

class AuthorResponse(AuthorCreate):
    author_id: int

    class Config:
        orm_mode = True

class BookResponse(BookCreate):
    book_id: int
    author: AuthorResponse

    class Config:
        orm_mode = True


@app.post("/authors/", response_model=AuthorResponse)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = Author(author_name=author.author_name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


@app.post("/books/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(
        book_name=book.book_name,
        book_description=book.book_description,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@app.get("/books/", response_model=list[BookResponse])
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.book_id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.get("/authors/", response_model=list[AuthorResponse])
def get_authors(db: Session = Depends(get_db)):
    return db.query(Author).all()


@app.get("/authors/{author_id}", response_model=AuthorResponse)
def get_author(author_id: int, db: Session = Depends(get_db)):
    db_author = db.query(Author).filter(Author.author_id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author
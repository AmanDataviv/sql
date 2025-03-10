from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Author(Base):
    __tablename__ = 'authors'

    author_id = Column(Integer, primary_key=True, index=True)
    author_name = Column(String, index=True)

    books = relationship("Book", back_populates="author")

class Book(Base):
    __tablename__ = 'books'

    book_id = Column(Integer, primary_key=True, index=True)
    book_name = Column(String, index=True)
    book_description = Column(String)
    author_id = Column(Integer, ForeignKey('authors.author_id'))

    author = relationship("Author", back_populates="books")
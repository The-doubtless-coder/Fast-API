from enum import Enum
from pydantic import BaseModel, validator
from datetime import date

class GenreUrlChoices(Enum): 
    @validator("genre", pre=True)
    def title_case_genre(cls, value):
        return value.title()
    ROCK = "Rock"
    ELECTRONIC = "Electronic"
    METAL = "Metal"
    HIPHOP = "Hip-hop"


class GenreModel(BaseModel):
    genre: GenreUrlChoices

    @validator("genre", pre=True)
    def title_case_genre(cls, value):
        if isinstance(value, str):
            return GenreUrlChoices(value.title())
        return value
   
   

class Album(BaseModel):
    id: int
    title: str
    release_date: date 

class Bands(BaseModel):
    id: int
    name: str
    genre: GenreUrlChoices
    album: list[Album] = []
    
class BandBase(BaseModel):
    name: str
    genre: GenreUrlChoices
    album: list[Album] = []

class BandCreate(BandBase):
    @validator("genre", pre=True)
    def title_case_genre(cls, value):
        return value.title() 

class BandWithID(BandBase):
    id: int

from fastapi import FastAPI, HTTPException
from schemas import GenreUrlChoices, Bands, BandCreate, BandWithID, GenreModel


app = FastAPI()


bands = [{"id":1, "name": "Judas Priest", "genre": "Metal", "album": [{"id": 1, "title": "pokemon", "release_date": "1970-01-01" }]}, 
        {"id":2, "name": "metallica", "genre": "Metal"}, 
        {"id":3, "name": "metallica", "genre": "Rock"}, 
        {"id":4, "name": "Sauti Sol", "genre": "Electronic"}, 
        {"id":5, "name": "Red Hot", "genre": "Metal"}]

@app.get("/hombre")
async def getHomePage() -> dict[str, str]:
    return {"is it available?": "I think not"}

@app.get("/about")
async def getAboutDetails() -> str:
    return "I am that I am just like Moses"

@app.get("/bands")
async def getAllBands() -> list[Bands]:
    return [
     Bands(**b) for b in bands
    ]

@app.post("/bands/query")
async def getBandsByGenreByQueryParams(genre: GenreModel | None = None, has_albums: bool = False) -> list[Bands]:
    band_list = [Bands(**b) for b in bands]

    if genre:
        band_list = [b for b in band_list if b.genre.value.lower() == genre.genre.value.lower()]
    if has_albums:
        band_list = [b for b in band_list if len(b.album) > 0]
    
    return band_list


@app.get("/bands/{band_id}", status_code= 200)
async def getSingleBand(band_id: int) ->Bands :
    band = next((Bands(**b) for b in bands if b["id"] == band_id), None)
    if(band is None):
        raise HTTPException(status_code=404, detail="band not found")
    return band


@app.get("/bands/genre/{genre}", status_code= 200)
async def getBandsByGenre(genre: GenreUrlChoices) ->list[Bands]:
    # band = next((b for b in bands if b["genre"] == genre), None)
    # if(band is None):
        # raise HTTPException(status_code=404, detail="band not found")
    return [
        Bands(**b) for b in bands if b['genre'].lower() == genre.value.lower()
    ]


@app.post("/bands")
async def createBand(band_data: BandCreate) -> BandWithID:
    id = bands[-1]["id"] + 1
    band = BandWithID(id=id, **band_data.model_dump()).model_dump()
    bands.append(band)
    return band

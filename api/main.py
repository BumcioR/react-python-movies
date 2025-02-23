from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import models
import schemas
from peewee import DoesNotExist, IntegrityError

app = FastAPI()

# Konfiguracja CORS
origins = [
    "http://localhost:3000", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

app.mount("/static", StaticFiles(directory="../ui/build/static", check_dir=False), name="static")

@app.get("/")
def serve_react_app():
    return FileResponse("../ui/build/index.html")

@app.get("/movies/", response_model=List[schemas.Movie])
def get_movies():
    try:
        movies = list(models.Movie.select())
        return movies
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching movies: {str(e)}")

@app.get("/movies/{movie_id}", response_model=schemas.Movie)
def get_movie(movie_id: int):
    try:
        movie = models.Movie.get(models.Movie.id == movie_id)
        return movie
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Movie not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching movie: {str(e)}")

@app.post("/movies/", response_model=schemas.Movie)
def add_movie(movie: schemas.MovieBase):
    try:
        new_movie = models.Movie.create(**movie.model_dump())
        return new_movie
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Movie already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding movie: {str(e)}")

@app.delete("/movies/{movie_id}", response_model=schemas.Movie)
def delete_movie(movie_id: int):
    try:
        movie = models.Movie.get(models.Movie.id == movie_id)
        movie.delete_instance()
        return movie
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Movie not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting movie: {str(e)}")

@app.get("/actors/", response_model=List[schemas.Actor])
def get_actors():
    try:
        actors = list(models.Actor.select())
        return actors
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching actors: {str(e)}")

@app.get("/actors/{actor_id}", response_model=schemas.Actor)
def get_actor(actor_id: int):
    try:
        actor = models.Actor.get(models.Actor.id == actor_id)
        return actor
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Actor not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching actor: {str(e)}")

@app.post("/actors/", response_model=schemas.Actor)
def add_actor(actor: schemas.ActorBase):
    try:
        new_actor = models.Actor.create(**actor.model_dump())
        return new_actor
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Actor already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding actor: {str(e)}")

@app.delete("/actors/{actor_id}", response_model=schemas.Actor)
def delete_actor(actor_id: int):
    try:
        actor = models.Actor.get(models.Actor.id == actor_id)
        actor.delete_instance()
        return actor
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Actor not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting actor: {str(e)}")

@app.post("/movies/{movie_id}/actors", response_model=schemas.Movie)
def update_actor(movie_id: int, actor_data: schemas.ActorToMovie):
    try:
        movie = models.Movie.get(models.Movie.id == movie_id)
        actor = models.Actor.get(models.Actor.id == actor_data.actor_id)
        movie.add_actor(actor)
        movie.save()
        return movie
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Movie or Actor not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding actor to movie: {str(e)}")

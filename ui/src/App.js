import "./App.css";
import { useEffect, useState } from "react";
import "milligram";
import MovieForm from "./MovieForm";
import MoviesList from "./MoviesList";
import ActorForm from "./ActorForm";
import ActorsList from "./ActorsList";
import AddActorToMovieForm from "./AddActorToMovieForm";

function App() {
  const [movies, setMovies] = useState([]);
  const [actors, setActors] = useState([]);
  const [addingMovie, setAddingMovie] = useState(false);
  const [addingActor, setAddingActor] = useState(false);

  const [addingActorToMovie, setAddingActorToMovie] = useState(false);

  async function handleAddMovie(movie) {
    const response = await fetch("/movies/", {
      method: "POST",
      body: JSON.stringify(movie),
      headers: { "Content-Type": "application/json" },
    });
    if (response.ok) {
      const movieFromServer = await response.json();
      setMovies((prevMovies) => [...prevMovies, movieFromServer]);
      setAddingMovie(false);
    }
  }

  async function handleDeleteMovie(movie) {
    const response = await fetch(`/movies/${movie.id}`, {
      method: "DELETE",
    });
    if (response.ok) {
      setMovies((prevMovies) => prevMovies.filter((m) => m.id !== movie.id));
    }
  }

  async function handleAddActor(actor) {
    const response = await fetch("/actors/", {
      method: "POST",
      body: JSON.stringify(actor),
      headers: { "Content-Type": "application/json" },
    });
    if (response.ok) {
      const actorFromServer = await response.json();
      setActors((prevActors) => [...prevActors, actorFromServer]);
      setAddingActor(false);
    }
  }

  async function handleDeleteActor(actor) {
    const response = await fetch(`/actors/${actor.id}`, {
      method: "DELETE",
    });
    if (response.ok) {
      setActors((prevActors) => prevActors.filter((a) => a.id !== actor.id));
    }
  }

  async function handleAddActorToMovie(movie_id, actor_id) {
    const response = await fetch(`/movies/${movie_id}/actors`, {
      method: "POST",
      body: JSON.stringify({ actor_id }),
      headers: { "Content-Type": "application/json" },
    });
    if (response.ok) {
      const updatedMovie = await response.json();
      setMovies((prevMovies) =>
        prevMovies.map((m) => (m.id === movie_id ? updatedMovie : m))
      );
      setAddingActorToMovie(false);
    }
  }

  useEffect(() => {
    const fetchMovies = async () => {
      const response = await fetch(`/movies/`);
      if (response.ok) {
        const movies = await response.json();
        setMovies(movies);
      }
    };
    const fetchActors = async () => {
      const response = await fetch(`/actors`);
      if (response.ok) {
        const actors = await response.json();
        setActors(actors);
      }
    };
    fetchMovies();
    fetchActors();
  }, [addingActorToMovie]);

  return (
    <div className="container">
      <h1>My favourite movies to watch</h1>
      {movies.length === 0 ? (
        <p>No movies yet?</p>
      ) : (
        <MoviesList movies={movies} onDeleteMovie={handleDeleteMovie} />
      )}
      {addingMovie ? (
        <MovieForm onMovieSubmit={handleAddMovie} buttonLabel="Add movie" />
      ) : (
        <button onClick={() => setAddingMovie(true)}>Add movie</button>
      )}
      {actors.length === 0 ? (
        <p>No actors yet?</p>
      ) : (
        <ActorsList actors={actors} onDeleteActor={handleDeleteActor} />
      )}
      {addingActor ? (
        <ActorForm onActorSubmit={handleAddActor} buttonLabel="Add an actor" />
      ) : (
        <button onClick={() => setAddingActor(true)}>Add an actor</button>
      )}
      <div>
        {addingActorToMovie ? (
          actors.length === 0 || movies.length === 0 ? (
            <p>You can add more</p>
          ) : (
            <AddActorToMovieForm
              onAddATMFSubmit={handleAddActorToMovie}
              buttonLabel="Add"
              movies={movies}
              actors={actors}
            />
          )
        ) : (
          <button onClick={() => setAddingActorToMovie(true)}>
            Add Actors to Movies
          </button>
        )}
      </div>
    </div>
  );
}

export default App;

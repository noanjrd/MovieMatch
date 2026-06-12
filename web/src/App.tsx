import { useState } from 'react'
import './App.css'

const Genres = {
  Drama: 'Drama',
  Comedy: 'Comedy',
  Thriller: 'Thriller',
  Family: 'Family',
  Adventure: 'Adventure',
  Fantasy: 'Fantasy',
  Science_Fiction: 'Science Fiction',
  Crime: 'Crime',
  Romance: "Romance",
  History : 'History',
  Mystery : 'Mystery',
} as const;

interface Movie {
  id: number;
  title: string;
  poster_link: string;
  genres?: string[];
}

const MovieCard = ({ movie, size = "small" }: { movie: Movie, size?: "small" | "large" }) => (
  <div className={`group relative flex-shrink-0 transition-transform duration-300 hover:scale-105 hover:z-200 ${size === "large" ? "w-48" : "w-40"}`}>
    <div className="aspect-[2/3] overflow-hidden rounded-xl bg-gray-800 shadow-lg  ">
      <img 
        src={movie.poster_link} 
        alt={movie.title}
        className="h-full w-full object-cover"
        loading="lazy"
      />
      <div className="absolute inset-0 bg-linear-to-t from-black/80 
      via-transparent to-transparent opacity-0 transition-opacity duration-300 flex flex-col justify-end p-3">
        <p className="text-white text-xs font-medium line-clamp-2">{movie.title}</p>
      </div>
    </div>
    <p className="mt-2 text-sm text-gray-300 font-medium truncate  transition-colors px-1">
      {movie.title}
    </p>
  </div>
);

function App() {
  const [input, setInput] = useState<string>("")
  const [moviesRecommended, setMoviesRecommended] = useState<Movie[]>([])
  const [moviesLikedByUser, setMoviesLikedByUser] = useState<Movie[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [currentUserId, setCurrentUserId] = useState<null | number>(null)

  const fetchRecommendations = async () => {
    if (!input || Number(input) === 0) return;
    setLoading(true)
    setError(null)
    const userId = Number(input)
    try {
      const backUrl = import.meta.env.VITE_BACK_URL;
      const url = backUrl  + "/users/" + input
      const answer = await fetch(url)
      const data = await answer.json()
      if (data.success) {
        setMoviesRecommended(data.movies_recommended || [])
        setMoviesLikedByUser(data.movies_liked_by_user || [])
        setCurrentUserId(userId)
      }
      else {
        setError(data.message || "An error occurred while fetching recommendations.")
        setMoviesRecommended([])
        setMoviesLikedByUser([])
      }
    } catch (error) {
      console.error("Failed to fetch:", error)
      setError("Failed to connect to the server.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-[#08060d] text-gray-100 font-sans">
      {/* Header / Search Section */}
      <header className="sticky top-0 z-250 bg-[#08060d]/80 backdrop-blur-md border-b border-gray-800/50 px-6 py-4">
        {error && (
          <div className="absolute top-full left-0 right-0 bg-red-500/90 text-white text-xs py-2 px-4 text-center animate-in fade-in slide-in-from-top-2">
            ⚠️ {error}
          </div>
        )}
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">

            <h1 className="text-2xl font-black bg-linear-to-r from-white to-gray-400 bg-clip-text text-transparent">
              MovieMatch
            </h1>
          </div>

          <div className="flex w-full md:w-auto items-center gap-2 bg-gray-900/50 p-1.5 rounded-full border border-gray-800 focus-within:border-purple-500/50 transition-all">
            <input 
              placeholder="Enter User ID (ex: 1)"
              className="bg-transparent border-none focus:ring-0 text-sm px-4 py-2 w-full md:w-64 outline-none"
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && fetchRecommendations()}
              type='number'
            />
            <button
              disabled={loading}
              onClick={fetchRecommendations}
              className="bg-purple-600 hover:bg-purple-500 disabled:opacity-50 text-white px-6 py-2 rounded-full text-sm font-semibold transition-all shadow-lg shadow-purple-600/20 shrink-0 flex items-center gap-2"
            >
              {loading && <div className="loading-spinner" />}
              {loading ? "Searching..." : "Get Recommendations"}
            </button>
          </div>
        </div>
      </header>
      <main className="max-w-7xl mx-auto px-6 py-8 flex flex-col gap-12">
        {/* Liked Movies Section */}
        {moviesLikedByUser.length > 0 && (
          <section className="animate-in fade-in slide-in-from-bottom-4 duration-700">
            <div className="flex items-center gap-2 mb-6">
              <span className="w-1.5 h-6  bg-purple-500 rounded-full"></span>
              <h3 className="text-xl  font-bold">Some movies user {currentUserId} has liked</h3>
            </div>
            <div className="flex gap-4 overflow-x-auto pb-4  ">
              {moviesLikedByUser.map((movie, idx) => (
                <MovieCard key={idx} movie={movie} size="large" />
              ))}
            </div>
          </section>
        )}

        {/* Title for Recommendations */}
        {moviesRecommended.length > 0 && (
          <div className="pt-8">
            <h2 className="text-2xl font-bold">What the algorithm thinks user {currentUserId} might like</h2>
          </div>
        )}

        {/* Recommendations Section */}
        {moviesRecommended.length > 0 ? (
          <div className="animate-in fade-in slide-in-from-bottom-4 duration-700">
            {Object.values(Genres).map((genre) => {
              const genreMovies = moviesRecommended.filter((m) => m.genres?.includes(genre));
              if (genreMovies.length === 0) return null;

              return (
                <section key={genre} className="animate-in fade-in slide-in-from-bottom-4 duration-700 delay-150">
                  <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center gap-3">
                      <span className="w-1.5 h-6 bg-blue-500 rounded-full"></span>
                      <h3 className="text-xl font-bold">{genre}</h3>
                    </div>
                    <span className="text-sm text-gray-500">{genreMovies.length} recommendations</span>
                  </div>
                  <div className="flex gap-4 overflow-x-auto pb-4  ">
                    {genreMovies.map((movie, idx) => (
                      <MovieCard key={idx} movie={movie} />
                    ))}
                  </div>
                </section>
              );
            })}
          </div>
        ) : !loading && (
          <div className="flex flex-col items-center justify-center py-20 text-center opacity-50">
            <div className="text-6xl mb-4">🍿</div>
            <h2 className="text-xl font-medium">No results yet</h2>
            <p className="text-gray-400 max-w-sm">Enter a user ID above to see personalized movie 
              recommendations based on the algorithm.</p>
          </div>
        )}
      </main>

      {/* AI Attribution Footer */}
      <footer className="max-w-7xl mx-auto px-6 py-12 border-t border-gray-900/50 mt-12 flex flex-col items-center gap-2">
        <div className="flex items-center gap-2 px-3 py-1 bg-purple-500/10 border border-purple-500/20 rounded-full">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-purple-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-purple-500"></span>
          </span>
          <p className="text-[10px] font-medium uppercase tracking-wider text-purple-400">
            Front-end crafted with AI
          </p>
        </div>
        <p className="text-gray-600 text-xs mt-2">
          Built to explore recommendation systems
        </p>
      </footer>
    </div>
  )
}

export default App

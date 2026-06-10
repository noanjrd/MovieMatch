import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'

const Genres = {
  Comedy: 'Comedy',
  Adventure: 'Adventure',
  Fantasy: 'Fantasy',
  Family: 'Family',
  Science_Fiction : 'Science Fiction',
  Thriller : 'Thriller',
  Crime : 'Crime',
  Romance : "Romance"
} as const;

function App() {
  const [input, setInput] = useState<string>("")
  const [movies, setMovies] = useState<any>([])

  const fetch_something = async () => {
    const url = "http://127.0.0.1:8000/users/" + input
    const answer = await fetch(url, {
      method: "GET"
    })
    const data = await answer.json()
    console.log(data.movies)
    setMovies(data.movies)
    console.log(movies)
  }


  return (
    <>
      <section id="center">
        <div className="hero">
          <img src={heroImg} className="base" width="170" height="179" alt="" />
          <img src={reactLogo} className="framework" alt="React logo" />
          <img src={viteLogo} className="vite" alt="Vite logo" />
        </div>
        <div>
          <h1>Get started</h1>
          <p>
            Edit <code>src/App.tsx</code> and save to test <code>HMR</code>
          </p>
        </div>
        <input onChange={(e) => { setInput(e.target.value) }}>
        </input>
        <button
          type="button"
          className="counter"
          onClick={fetch_something}
        >
          Get recommendations
        </button>
        <div className='grid grid-rows gap-5'>
          {Object.values(Genres).map((genre: any, index: number) => (
            <div>
              <p className='text-left text-white font-bold text-2xl'>{genre}</p>
              <div key={index} className='grid grid-cols-6 gap-2  overflow-y-auto mt-4 '>
                {movies.filter((movie: any) => movie.genres?.includes(genre)).map((movie: any, index: number) => (
                    <div key={index}>
                      <img src={movie.poster_link} className='h-55 w-full object-cover' />
                      <p className='text-white'>

                        {movie.title}
                      </p>
                    </div>
                  ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      <div className="ticks"></div>

    </>
  )
}

export default App

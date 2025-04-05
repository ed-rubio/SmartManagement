import { useState } from 'react'
import './App.css'
import NavBar from '../'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <h1> Hola  tonotos</h1>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edita <code>src/Tumama.jxs</code> y guarda para no reprobar
        </p>
      </div>
      <p className="read-the-docs">
        Click aqui si eres gei
      </p>
    </>
  )
}

export default App

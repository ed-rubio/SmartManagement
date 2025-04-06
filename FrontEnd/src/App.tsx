import './index.css'

function App() {

  return (
    <>
    <div className='items-center justify-center'>
      <section className='bg-blue-950 p-4 shadow-md w-full'>
      <h1 className='text-3xl text-white font-bold text-center'>
        Jeje Hola
      </h1>
      </section>
      <div className='w-full items-center justify-center'>
        <button onClick={() => alert('Edita esto o eres puto')} className='bg-blue-500 text-white p-2 mt-4'>
          CLick me
        </button>
      </div>
    </div>
    </>
  )
}

export default App

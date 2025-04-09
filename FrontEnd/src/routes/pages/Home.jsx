import { Link } from "react-router-dom";


const Home = ({ user, setUser }) => {
  const handleLogout = () => {
    localStorage.removeItem("user");
    setUser([]);
  };

  return (
    <div className="w-full min-h-screen bg-white text-gray-800">
      {/* Hero Section */}
      <section className="w-full h-[60vh] bg-Base flex flex-col items-center justify-center text-center px-6 py-5">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          Evita pérdidas. Optimiza tus pedidos.
        </h1>
        <p className="text-lg md:text-xl mb-6 max-w-2xl">
          Nuestra app web te ayuda a calcular la cantidad ideal de productos a pedir,
          reduciendo el sobreinventario y minimizando costos.
        </p>
        <Link to='/instrucciones' className='mn-link'>
        <button className="bg-blue-600 text-white px-6 py-3 rounded-2xl hover:bg-blue-700 transition">
          Ver cómo funciona
        </button>
        </Link>
      </section>

      {/* Beneficios */}
      <section className="py-16 px-6 bg-gray-50 text-center">
        <h2 className="text-3xl font-semibold mb-10">¿Por qué usar nuestra app?</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-10 max-w-6xl mx-auto">
          <div>
            <div className="text-5xl mb-4">📦</div>
            <h3 className="text-xl font-bold mb-2">Menos sobreinventario</h3>
            <p className="text-gray-600">Evita comprar más de lo necesario y reduce productos estancados.</p>
          </div>
          <div>
            <div className="text-5xl mb-4">📊</div>
            <h3 className="text-xl font-bold mb-2">Análisis inteligente</h3>
            <p className="text-gray-600">Considera demanda, costos y mantenimiento en cada recomendación.</p>
          </div>
          <div>
            <div className="text-5xl mb-4">⚙️</div>
            <h3 className="text-xl font-bold mb-2">Automatización</h3>
            <p className="text-gray-600">Optimiza pedidos sin cálculos manuales, con un clic.</p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;

const Home = ({ user, setUser }) => {
 
  const handleLogout = () => {
    // Limpiar el localStorage
    localStorage.removeItem('user');
    setUser([]);
  };

  return (
    <div>
      <h1>Bienvenido</h1>
      <h2>{user}</h2>
      <button onClick={handleLogout}>Cerrar sesión</button>
    </div>
  );
}
export default Home;
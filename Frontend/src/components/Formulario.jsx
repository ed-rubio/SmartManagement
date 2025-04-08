import "./Formulario.css";
import { useState } from "react";

export function Formulario({ setUser }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(false);
  const [mensajeError, setMensajeError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (username.trim() === "" || password.trim() === "") {
      setError(true);
      setMensajeError("Todos los campos son obligatorios");
      return;
    }

    setError(false);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/v0/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (response.ok) {
        if (data.message === "Inicio de sesión exitoso" && data.user) {
          setUser([data.user.username]); // Establece el username del usuario
        } else {
          setError(true);
          setMensajeError(data.error || "Error desconocido al iniciar sesión");
        }
      } else {
        setError(true);
        setMensajeError(data.error || "Credenciales incorrectas");
      }
    } catch (err) {
      setError(true);
      setMensajeError("Error al conectar con el servidor");
    }
  };

  return (
    <section>
      <h1>SmartManagement</h1>

      <form className="formulario" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Usuario"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button>Iniciar sesión</button>
      </form>

      {error && <p className="error">{mensajeError}</p>}
    </section>
  );
}
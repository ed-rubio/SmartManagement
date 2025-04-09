import { useNavigate } from 'react-router-dom';

const HowTo = () => {
  const navigate = useNavigate();

  return (
    <section className="w-full min-h-screen bg-white px-6 py-12 flex flex-col items-center text-gray-800">
      <div className="max-w-3xl text-center">
        <h1 className="text-4xl font-bold mb-4 text-blue-600">
          ¿Cómo usar la herramienta de pedidos óptimos?
        </h1>
        <p className="text-lg mb-10">
          Sigue estos pasos para calcular la <strong>Cantidad Económica de Pedido (EOQ)</strong> y minimizar tus costos de inventario:
        </p>

        <div className="text-left space-y-6">
          <div>
            <h2 className="text-2xl font-semibold mb-1">1. Busca un producto</h2>
            <p>Escribe el nombre del producto que deseas analizar. Aparecerán sugerencias automáticas según lo que escribas.</p>
          </div>

          <div>
            <h2 className="text-2xl font-semibold mb-1">2. Selecciónalo</h2>
            <p>Haz clic en el producto que deseas agregar a la tabla de análisis.</p>
          </div>

          <div>
            <h2 className="text-2xl font-semibold mb-1">3. Ajusta la demanda</h2>
            <p>Indica cuántas unidades vendes (o usas) al mes. Esto nos ayudará a estimar la demanda mensual.</p>
          </div>

          <div>
            <h2 className="text-2xl font-semibold mb-1">4. Calcula el EOQ</h2>
            <p>Haz clic en <strong>“Calcular EOQ”</strong> para obtener recomendaciones automáticas de cuántas unidades pedir y cada cuánto hacerlo.</p>
          </div>

          <div>
            <h2 className="text-2xl font-semibold mb-1">5. Consulta los costos</h2>
            <p>Se mostrará un resumen con el costo total estimado: envío, impuestos y costo de inventario.</p>
          </div>
        </div>

        <button
          onClick={() => navigate('/math')}
          className="mt-10 bg-blue-600 text-white px-8 py-3 rounded-2xl text-lg hover:bg-blue-700 transition"
        >
          Ir a la Calculadora
        </button>
      </div>
    </section>
  );
};

export default HowTo;

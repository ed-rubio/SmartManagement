
import '../../CSS/Math.css';
import React, { useState, useEffect, useCallback } from 'react';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v0';

// -------------------------------------------------------------------------- //

// ¿Y si me ven como un hazmerreír, como un loco descerebrado?
// Aunque no andarían muy desencaminados.
//                                         - Solaire de Astora

// -------------------------------------------------------------------------- //

const MathScreen = () => {
    const [ searchTerm, setSearchTerm ] = useState('');
    const [ searchResults, setSearchResults ] = useState([]);
    const [ selectedProducts, setSelectedProducts ] = useState([]);
    const [ showSuggestions, setShowSuggestions ] = useState(false);
    const [ resultsEOQ, setResultsEOQ ] = useState({});
    const [ orderTotalCost, setOrderTotalCost ] = useState(null);

    // Búsqueda de productos:
    const fetchProducts = useCallback(async (searchTerm) => {
        if (!searchTerm) {
            setSearchResults([]);
            setShowSuggestions(false);
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/search/?search=${searchTerm}`);
            if (!response.ok) {
                throw new Error(`ERROR: Status: ${response.status}`);
            }
            const data = await response.json();
            setSearchResults(data);
            setShowSuggestions(true);
        } catch (error) {
            setShowSuggestions(false);
        }
    }, [API_BASE_URL]);

    const handleInputChange = (event) => {
        const newSearchTerm = event.target.value;
        setSearchTerm(newSearchTerm);
        fetchProducts(newSearchTerm);
    };

    const handleSelectProduct = (product) => {
        const alreadySelected = selectedProducts.some(
            (selectedProduct) => selectedProduct.sku === product.sku
        );

        if (!alreadySelected) {
            setSelectedProducts([...selectedProducts, { ...product, quantity: 1 }]);
            setSearchTerm('');
            setSearchResults([]);
            setShowSuggestions(false);
            setResultsEOQ({});
            setOrderTotalCost(null);
        } else {
            alert('¡Ojito! Este producto se encuentra seleccionado.');
        }
    };

    const handleRemoveProduct = (index) => {
        const skuToRemove = selectedProducts[index].sku;
        const newSelectedProducts = selectedProducts.filter((_, i) => i !== index);
        setSelectedProducts(newSelectedProducts);
        const newEoqResults = { ...resultsEOQ };
        delete newEoqResults[skuToRemove];
        setResultsEOQ(newEoqResults);
        setOrderTotalCost(null);
    };

    const handleQuantityChange = (index, newQuantity) => {
        const updatedProducts = selectedProducts.map((product, i) =>
            i === index ? { ...product, quantity: parseInt(newQuantity, 10) || 1 } : product
        );
        setSelectedProducts(updatedProducts);
        setResultsEOQ({});
        setOrderTotalCost(null);
    };

    const isValidPositiveNumber = (value) => {
        return typeof value === 'number' && !isNaN(value) && value > 0;
    };


    // DERIVACIÓN... Plim plim plom... plim plom plim... plim plom... plom.
    const calculateEOQForProduct = (product) => {
        // Demanda mensual estimada (D).
        const monthlyDemand = parseInt(product.quantity, 10) || 1;

        // Costo de envío por pedido (S), basado en la demanda mensual.
        let orderingCost = 20; // 5 es el costo base.
 
        if (monthlyDemand > 10) {
            orderingCost += 5;
        }
        if (monthlyDemand > 30) {
            orderingCost += 15;
        }
        if (parseFloat(product.cost) > 50) {
            orderingCost += 15;
        }
        if (parseFloat(product.cost) > 100) {
            orderingCost += 20;
        }

        // Costo de mantenimiento por unidad (mensual) (H).
        // Notita: el costo anual de mantener el inventario es el 4% del valor del inventario (incluidos los impuestos).
        const holdingCostPerUnitMonth = (parseFloat(product.cost) * ((parseFloat(product.iva) + parseFloat(product.ieps)) / 100)) * (4 / 12);

        // -- PASO #01: ----------------------------------------------------- //
        // Primero vamos a definir la función: Costo total (mensual) del inventario.
        // CT(Q) = (D/Q) * S + (Q/2) * H

        // En esta fórmula:
            // D representa la demanda mensual del producto (monthlyDemand).
            // Q representa la cantidad de pedido óptima.
            // S representa el costo de envío (orderingCost).
            // H representa el costo de Mantenimiento por unidad (holdingCostPerUnitMonth).
    
        // CT(Q) = costoDeOrdenar(Q) + costoDeMantener(Q)
        const costoDeOrdenar = (Q) => (monthlyDemand / Q) * orderingCost;
        const costoDeMantener = (Q) => (Q / 2) * holdingCostPerUnitMonth;

        // -- PASO #02: ----------------------------------------------------- //
        // Procedemos a derivar CT(Q) con respecto a Q, e igualamos a cero para encontrar el punto crítico:
        // d(CT)/dQ = - (D * S) / Q^2 + H / 2 = 0

        // -- PASO #03: ----------------------------------------------------- //
        // Sumamos (D * S) / Q^2 a ambos lados:
        // H / 2 = (D * S) / Q^2
        const paso4_ladoIzquierdo = holdingCostPerUnitMonth / 2;
        const paso4_ladoDerecho_numerador = monthlyDemand * orderingCost;

        // -- PASO #04: ----------------------------------------------------- //
        // Multiplicamos ambos lados por Q^2 y dividimos por (H / 2) para despejar Q^2:
        // Q^2 = (D * S) / (H / 2)
        const qCuadrado = paso4_ladoDerecho_numerador / paso4_ladoIzquierdo;

        // -- PASO #05: ----------------------------------------------------- //
        // Tomamos la raíz cuadrada de ambos lados para obtener Q (EOQ):
        // Q = √((2 * D * S) / H)
        const economicOrderQuantity = Math.sqrt(qCuadrado);

        // -- PASO #06: ----------------------------------------------------- //
        // Y pue'... los siguientes utilizan el valor de EOQ encontrado.

        const optimalNumberOfOrdersYear = isValidPositiveNumber(economicOrderQuantity) && monthlyDemand > 0 ? (monthlyDemand * 12) / economicOrderQuantity : 0;
        const timeBetweenOrdersMonths = isValidPositiveNumber(optimalNumberOfOrdersYear) ? 12 / optimalNumberOfOrdersYear : 0;
        const totalInventoryCostMonth = isValidPositiveNumber(economicOrderQuantity) ?
            costoDeOrdenar(economicOrderQuantity) + costoDeMantener(economicOrderQuantity) : 0;

        return {
            economicOrderQuantity: Math.round(economicOrderQuantity),
            monthlyDemand: monthlyDemand,
            orderingCost: orderingCost.toFixed(2),
            holdingCostPerUnitMonth: holdingCostPerUnitMonth.toFixed(2),
            optimalNumberOfOrdersYear: optimalNumberOfOrdersYear.toFixed(2),
            timeBetweenOrdersMonths: timeBetweenOrdersMonths.toFixed(2),
            totalInventoryCostMonth: totalInventoryCostMonth.toFixed(2),
        };
    };

    const calculateAllEOQAndOrderCost = () => {
        const eoqResults = {};
        let totalShippingCost = 0;
        let subtotalCost = 0;
        let totalIva = 0;
        let totalIeps = 0;
        let totalCost = 0;
    
        selectedProducts.forEach(product => {
            const eoqData = calculateEOQForProduct(product);
            eoqResults[product.sku] = eoqData;
    
            if (eoqData && !eoqData.error && isValidPositiveNumber(eoqData.economicOrderQuantity)) {
                // Sumar el costo de envío para este producto
                totalShippingCost += eoqData.orderingCost ? parseFloat(eoqData.orderingCost) : 0;
    
                // Calcular el costo del producto sin impuestos
                const baseProductCost = parseFloat(product.cost);
                const quantityToOrder = eoqData.economicOrderQuantity;
                const productSubtotal = baseProductCost * quantityToOrder;
                subtotalCost += productSubtotal;
    
                // Calcular el IVA para este producto
                const ivaRate = parseFloat(product.iva) / 100;
                const productIva = productSubtotal * ivaRate;
                totalIva += productIva;
    
                // Calcular el IEPS para este producto
                const iepsRate = parseFloat(product.ieps) / 100;
                const productIeps = productSubtotal * iepsRate;
                totalIeps += productIeps;
            }
        });
    
        totalCost = subtotalCost + totalIva + totalIeps + totalShippingCost;
    
        setResultsEOQ(eoqResults);
        setOrderTotalCost({
            shipping: totalShippingCost.toFixed(2),
            subtotal: subtotalCost.toFixed(2),
            iva: totalIva.toFixed(2),
            ieps: totalIeps.toFixed(2),
            total: totalCost.toFixed(2),
        });
    };

    return (
        <section className='math-section'>
            <strong className='math-title'>CANTIDAD ECONÓMICA DE PEDIDO (Cálculos Mensuales)</strong>

            <div className='math-products'>
                <div className='math-products-search'>
                    <strong className='math-subtitle'>PRODUCTOS</strong>
                    <div className='math-products-search-input'>
                        <input
                            type='text'
                            placeholder='Buscar producto...'
                            className='math-input'
                            value={searchTerm}
                            onChange={handleInputChange}
                            maxLength={16}
                            onFocus={() => searchTerm && searchResults.length > 0 && setShowSuggestions(true)}
                            onBlur={() => setTimeout(() => setShowSuggestions(false), 100)}
                        />
                        {showSuggestions && searchResults.length > 0 && (
                            <div className='math-products-search-suggestions'>
                                <ul>
                                    {searchResults.map((product, index) => (
                                        <li key={index} onClick={() => handleSelectProduct(product)}>
                                            {product.name}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        )}
                    </div>
                </div>

                <div className='math-products-selected'>
                    {selectedProducts.length > 0 ? (
                        <table className='math-products-selected-table'>
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Nombre</th>
                                    <th>Cantidad estimada</th>
                                    <th>Costo de almacén</th>
                                    <th>Precio</th>
                                    <th>IVA</th>
                                    <th>IEPS</th>
                                    <th>Acciones</th>
                                </tr>
                            </thead>
                            <tbody>
                                {selectedProducts.map((product, index) => {
                                    const product_quantity = parseInt(product.quantity || 1);
                                    const product_wh_cost = (parseFloat(product.cost) * ((parseFloat(product.iva) + parseFloat(product.ieps)) / 100)) * 4;
                                    const eoqData = resultsEOQ[product.sku];

                                    return (
                                        <tr key={index}>
                                            <td>{index + 1}</td>
                                            <td>{product.name}</td>
                                            <td>
                                                <input
                                                    type='number'
                                                    value={product_quantity}
                                                    onChange={(e) => handleQuantityChange(index, parseInt(e.target.value))}
                                                />
                                            </td>
                                            <td>{product_wh_cost.toFixed(2)}</td>
                                            <td>{product.cost}</td>
                                            <td>{product.iva} %</td>
                                            <td>{product.ieps} %</td>
                                            <td>
                                                <button className='remove-button ' onClick={() => handleRemoveProduct(index)}>
                                                    Eliminar
                                                </button>

                                                {eoqData && !eoqData.error ? (
                                                    <button className='eoq-button' onClick={() => alert(
                                                        `EOQ para ${product.name}:\n` +
                                                        `Cantidad Óptima (mensual): ${eoqData.economicOrderQuantity} unidades\n` +
                                                        `Demanda Mensual: ${eoqData.monthlyDemand} unidades\n` +
                                                        `Costo de Pedido: $${eoqData.orderingCost}\n` +
                                                        `Costo de Mantenimiento por Unidad (mensual): $${eoqData.holdingCostPerUnitMonth}\n` +
                                                        `Número Óptimo de Pedidos por Año (aprox.): ${eoqData.optimalNumberOfOrdersYear}\n` +
                                                        `Tiempo entre Pedidos (meses): ${eoqData.timeBetweenOrdersMonths}\n` +
                                                        `Costo Total de Inventario (mensual, aprox.): $${eoqData.totalInventoryCostMonth}`
                                                    )}>
                                                        Ver EOQ
                                                    </button>
                                                ) : eoqData?.error ? (
                                                    <span className='eoq-error-text'>{eoqData.error}</span>
                                                ) : (
                                                    <span className='text-random'>Sin calcular (EOQ)</span>
                                                )}
                                            </td>
                                        </tr>
                                    );
                                })}
                            </tbody>
                        </table>
                    ) : (
                        <strong>No se ha seleccionado ningún producto.</strong>
                    )}
                </div>
            </div>

            {selectedProducts.length > 0 && (
                <div className='math-eoq-results'>
                    <button onClick={calculateAllEOQAndOrderCost} className='calculate-button'>Calcular EOQ</button>

                    {orderTotalCost !== null && (
                        <div className='order-total-cost'>
                            <strong>Envío: <small>${orderTotalCost.shipping}</small></strong>
                            <strong>Subtotal: <small>${orderTotalCost.subtotal}</small></strong>
                            <strong>IVA: <small>${orderTotalCost.iva}</small></strong>
                            <strong>IEPS: <small>${orderTotalCost.ieps}</small></strong>
                            <strong>Total: <small>${orderTotalCost.total}</small></strong>
                        </div>
                    )}
                </div>
            )}
        </section>
    );
}

export default MathScreen;
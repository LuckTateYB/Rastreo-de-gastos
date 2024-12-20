document.addEventListener("DOMContentLoaded", function () {
  // Seleccionamos el formulario
  const expenseForm = document.getElementById("expenseForm");

  // Escuchamos el evento de envío del formulario
  expenseForm.addEventListener("submit", function (event) {
    event.preventDefault(); // Prevenimos que la página se recargue

    // Obtenemos los valores de los campos del formulario
    const descripcion = document.getElementById("descripcion").value;
    const monto = document.getElementById("amount").value;
    const categoria = document.getElementById("category").value;
    const fecha = document.getElementById("date").value;

    // Validamos los campos
    if (!descripcion || !monto || !categoria || !fecha) {
      alert("Por favor, completa todos los campos.");
      return;
    }

    // Enviamos los datos al backend
    fetch("/agregar_gasto", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ descripcion, monto, categoria, fecha }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          alert(data.error);
        } else {
          alert(data.message);
          listarGastos(); // Actualizamos la lista de gastos
        }
      })
      .catch((error) => console.error("Error:", error));
  });

  // Función para listar los gastos
  function listarGastos() {
    fetch("/listar_gastos")
      .then((response) => response.json())
      .then((data) => {
        const expensesList = document.getElementById("expensesList");
        expensesList.innerHTML = ""; // Limpiamos la lista

        // Creamos elementos para cada gasto
        data.forEach((gasto) => {
          const row = document.createElement("tr");

          // Celda para la descripción
          const descripcionCell = document.createElement("td");
          descripcionCell.textContent = gasto.descripcion;
          row.appendChild(descripcionCell);

          // Celda para el monto
          const montoCell = document.createElement("td");
          montoCell.textContent = `S/${parseFloat(gasto.monto).toFixed(2)}`;
          row.appendChild(montoCell);

          // Celda para la categoría
          const categoriaCell = document.createElement("td");
          categoriaCell.textContent = gasto.categoria;
          row.appendChild(categoriaCell);

          // Celda para la fecha
          const fechaCell = document.createElement("td");
          fechaCell.textContent = gasto.fecha;
          row.appendChild(fechaCell);

          // Agregamos la fila a la tabla
          expensesList.appendChild(row);
        });
      })
      .catch((error) => console.error("Error al listar los gastos:", error));
  }

  // Cargamos la lista de gastos al cargar la página
  listarGastos();
});

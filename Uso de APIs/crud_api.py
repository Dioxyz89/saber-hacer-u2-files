"""Cliente Python para consumir una API REST (operaciones CRUD)."""
import requests  # type: ignore

BASE_URL = "http://127.0.0.1:5000/api/productos"
HEADERS = {"X-API-Key": "demo-key-123", "Content-Type": "application/json"}
TIMEOUT = 10


def mostrar(respuesta):
    """Imprime el codigo de estado y el cuerpo de la respuesta."""
    print(f"Estado: {respuesta.status_code} {respuesta.reason}")
    try:
        print(respuesta.json())
    except ValueError:
        print("(sin cuerpo JSON)")
    return respuesta


def agregar(producto):
    """CREATE - POST: agrega un nuevo producto."""
    r = requests.post(BASE_URL, json=producto, headers=HEADERS, timeout=TIMEOUT)
    return mostrar(r)


def buscar(id_producto=None):
    """READ - GET: lista todos los productos o busca uno por id."""
    url = BASE_URL if id_producto is None else f"{BASE_URL}/{id_producto}"
    r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    return mostrar(r)


def actualizar(id_producto, cambios):
    """UPDATE - PUT: modifica los datos de un producto existente."""
    r = requests.put(f"{BASE_URL}/{id_producto}", json=cambios,
                     headers=HEADERS, timeout=TIMEOUT)
    return mostrar(r)


def eliminar(id_producto):
    """DELETE - DELETE: elimina un producto por id."""
    r = requests.delete(f"{BASE_URL}/{id_producto}", headers=HEADERS, timeout=TIMEOUT)
    return mostrar(r)


if __name__ == "__main__":
    try:
        print("--- AGREGAR ---")
        agregar({"nombre": "Monitor 24 pulgadas", "precio": 2400.0, "stock": 8})
        print("--- BUSCAR ---")
        buscar(3)
        print("--- ACTUALIZAR ---")
        actualizar(3, {"precio": 2199.0, "stock": 12})
        print("--- ELIMINAR ---")
        eliminar(3)
        print("--- BUSCAR (ya eliminado) ---")
        buscar(3)
    except requests.exceptions.RequestException as e:
        print("Error de conexion:", e)

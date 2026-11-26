"""Servidor API REST de demostracion (solo biblioteca estandar)."""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

API_KEY = "demo-key-123"
productos = {
    1: {"id": 1, "nombre": "Teclado mecanico", "precio": 850.0, "stock": 15},
    2: {"id": 2, "nombre": "Mouse inalambrico", "precio": 320.0, "stock": 40},
}
siguiente_id = 3


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, data=None):
        body = json.dumps(data, ensure_ascii=False).encode() if data is not None else b""
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _auth(self):
        if self.headers.get("X-API-Key") != API_KEY:
            self._send(401, {"error": "API key inválida o ausente"})
            return False
        return True

    def _id(self):
        partes = self.path.strip("/").split("/")
        if partes[:2] != ["api", "productos"]:
            return "bad", None
        if len(partes) == 2:
            return "col", None
        try:
            return "item", int(partes[2])
        except ValueError:
            return "bad", None

    def _json(self):
        n = int(self.headers.get("Content-Length", 0))
        try:
            return json.loads(self.rfile.read(n) or b"{}")
        except json.JSONDecodeError:
            return None

    def do_GET(self):
        if not self._auth(): return
        t, i = self._id()
        if t == "col": return self._send(200, list(productos.values()))
        if t == "item" and i in productos: return self._send(200, productos[i])
        self._send(404, {"error": "Recurso no encontrado"})

    def do_POST(self):
        global siguiente_id
        if not self._auth(): return
        t, _ = self._id()
        if t != "col": return self._send(404, {"error": "Recurso no encontrado"})
        d = self._json()
        if not d or "nombre" not in d or "precio" not in d:
            return self._send(400, {"error": "Campos obligatorios: nombre, precio"})
        p = {"id": siguiente_id, "nombre": d["nombre"], "precio": d["precio"], "stock": d.get("stock", 0)}
        productos[siguiente_id] = p
        siguiente_id += 1
        self._send(201, p)

    def do_PUT(self):
        if not self._auth(): return
        t, i = self._id()
        if t != "item" or i not in productos:
            return self._send(404, {"error": "Recurso no encontrado"})
        d = self._json()
        if d is None: return self._send(400, {"error": "JSON mal formado"})
        productos[i].update({k: v for k, v in d.items() if k != "id"})
        self._send(200, productos[i])

    def do_DELETE(self):
        if not self._auth(): return
        t, i = self._id()
        if t != "item" or i not in productos:
            return self._send(404, {"error": "Recurso no encontrado"})
        del productos[i]
        self._send(200, {"mensaje": f"Producto {i} eliminado correctamente"})

    def do_PATCH(self):
        self._send(405, {"error": "Metodo no permitido"})


if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 5000), Handler).serve_forever()

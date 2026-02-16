from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse


class WebRequestHandler(BaseHTTPRequestHandler):
    def url(self):
        return urlparse(self.path)

    def query_data(self):
        return dict(parse_qsl(self.url().query))

    def do_GET(self):

        contenido = {}

        try:
            with open("home.html", "r", encoding="utf-8") as f:
                contenido["/"] = f.read()

            with open("1.html", "r", encoding="utf-8") as f:
                contenido["/proyecto/1"] = f.read()

            contenido["/proyecto/2"] = """
            <html>
                <h1>Proyecto 2</h1>
                <p>Contenido pendiente...</p>
                <a href="/">Regresar</a>
            </html>
            """

            contenido["/proyecto/3"] = """
            <html>
                <h1>Proyecto 3</h1>
                <p>Contenido pendiente...</p>
                <a href="/">Regresar</a>
            </html>
            """

        except FileNotFoundError:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"<h1>Error cargando archivos</h1>")
            return


        if self.path in contenido:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(contenido[self.path].encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"<h1>Error 404: Pagina no encontrada</h1>")
    
    def valida_autor(self):
        if "autor" in self.query_data():
            return True
        else:
            return False
    
    def get_html(self, path, qs):
        
        return f"""
        <h1>Proyecto: {path} Autor: {qs['autor']}</h1>
"""

    def get_response(self):
        return f"""
    <h1> Hola Web </h1>
    <p> URL Parse Result : {self.url()}         </p>
    <p> Path Original: {self.path}         </p>
    <p> Headers: {self.headers}      </p>
    <p> Query: {self.query_data()}   </p>
"""


if __name__ == "__main__":
    print("Starting server")
    server = HTTPServer(("localhost", 8000), WebRequestHandler)
    server.serve_forever()

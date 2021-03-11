from threading import Thread
from socketserver import ThreadingMixIn
from http.server import HTTPServer, BaseHTTPRequestHandler
import Monopolio as mp
import FrontMonopolio as fm
import json
from urllib.parse import urlparse
from urllib.parse import parse_qs


class ServerMonopolioBack(BaseHTTPRequestHandler):
    mmp = mp.Monopolio()

    def do_GET(self):
        parsed_url = urlparse(self.path)
        if parsed_url.path.endswith('/api/monopolio') or parsed_url.path.endswith('/api/monopolio.json'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            query_components = parse_qs(parsed_url.query)
            if query_components:
                if 'ms' in query_components:
                    self.mmp.max_simulacoes = int(query_components['ms'][0])
                if 'ndc' in query_components:
                    self.mmp.numero_de_casas = int(query_components['ndc'][0])
                if 'mr' in query_components:
                    self.mmp.max_rodadas = int(query_components['mr'][0])
                if 'mv' in query_components:
                    self.mmp.max_venda = float(query_components['mv'][0])
                if 'pmv' in query_components:
                    self.mmp.porcentagem_min_venda = float(query_components['pmv'][0])
                if 'pa' in query_components:
                    self.mmp.porcentagem_aluguel = float(query_components['pa'][0])
                if 'bdr' in query_components:
                    self.mmp.bonus_da_rodada = float(query_components['bdr'][0])
            self.mmp.simulacao()
            self.wfile.write(bytes(json.dumps(self.mmp.simulacao_dict), 'utf8'))
        return


class ServerMonopolioFront(BaseHTTPRequestHandler):
    ffm = fm.FrontMonopolio()

    def do_GET(self) -> None:

        if self.path.endswith('/form'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Read the file and send the contents
            with open('form.html', 'rb') as file:
                self.wfile.write(bytes(file.read(), 'utf8'))
        if self.path.endswith('/text'):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.ffm.get_simulacao()
            self.ffm.to_text()
            self.wfile.write(bytes(self.ffm.text_str, 'utf8'))
        elif self.path.endswith('/'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.ffm.get_simulacao()
            self.ffm.to_html()
            html = f"<html><head></head><body>{self.ffm.html_str}</body></html>"
            # Writing the HTML contents with UTF-8
            self.wfile.write(bytes(html, "utf8"))
        return

        # self.wfile.write("Hello World!")
        # self.wfile.write(bytes("Hello World! Front", "utf-8"))


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True


def serve_on_port(port, HTTPServer):
    server = ThreadingHTTPServer(("localhost", port), HTTPServer)
    print(f"INICIANDO: http://localhost:{port}")
    server.serve_forever()


Thread(target=serve_on_port, args=[9000, ServerMonopolioBack]).start()
Thread(target=serve_on_port, args=[8000,  ServerMonopolioFront]).start()
# serve_on_port(8000, ServerMonopolioFront)

import soundfile as sf
from os import path
import json
from tango import Tango

tango = Tango("local", "cpu")
# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "localhost"
serverPort = 8081
currDir = path.dirname(path.abspath(__file__))

class MyServer(BaseHTTPRequestHandler):
    def do_POST(self):
        if (self.path == '/'):
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            prompt = body.decode("utf-8")
            print(prompt)
            audio = tango.generate(prompt, 10, 3, 1, False)
            print("audio gfenerated. Saving...")
            sf.write(f"{prompt}.wav", audio, samplerate=16000)
            file_path = path.join(currDir, f"{prompt}.wav")
            json_data = {
                "filqePath": file_path
            }
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(json_data), "utf-8"))
        else:
          self.send_response(404)
          self.end_headers()
          self.wfile.write(bytes("Not found", "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

import soundfile as sf
from tango import Tango

tango = Tango("local", "cpu")
# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_POST(self):
        if (self.path == '/'):
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            prompt = body.decode("utf-8")
            audio = tango.generate(prompt)
            sf.write(f"{prompt}.wav", audio, samplerate=16000)
            self.send_response(200)
            self.send_header("Content-type", "audio/wav")
            self.end_headers()
            self.wfile.write(audio)
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
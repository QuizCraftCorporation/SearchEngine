import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from database import TextDataBase
import json

# Parsing command line arguments
parser = argparse.ArgumentParser(
    prog="Search engine",
    description="Simple search engine based on embeddings and vector store"
)
parser.add_argument('--address', help="Address of hosting (for example 127.0.0.1)", default="127.0.0.1")
parser.add_argument('--port', help="Port of service (for example 1234)", default=1234)

args = parser.parse_args()

HOST = args.address
PORT = int(args.port)

# Loading database
DATABASE = TextDataBase()

class DatabaseHTTP(BaseHTTPRequestHandler):
    """
    Class to handle HTTP request and utilize text database for searching.
    """
    
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Everything is up!", "utf-8"))
    
    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        if self.path == "/save":
            user_data = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            quiz_payload = user_data["raw_quiz_data"]
            unique_name = user_data["unique_id"]
            DATABASE.add_text(quiz_payload, unique_name)
            response = {}
            response["operation"] = "SUCCESS"
            self.wfile.write(bytes(json.dumps(response), "utf-8"))
        elif self.path == "/search":
            user_data = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            query = user_data["query"]
            k = user_data["number_of_results"]
            results = DATABASE.search(query, k)
            response = {}
            if results[0] == "ok":
                quizzes_data = []
                for result in results[1]:
                    quiz_data = {}
                    quiz_data["raw_quiz_data"] = result[0]
                    quiz_data["unique_id"] = result[1]
                    quizzes_data.append(quiz_data)    
                response["operation"] = "SUCCESS"
                response["payload"] = quizzes_data
            else:
                response["operation"] = "EMPTY"
            self.wfile.write(bytes(json.dumps(response), "utf-8"))
        else:
            response = {}
            response["operation"] = "FAILED"
            self.wfile.write(bytes(json.dumps(response), "utf-8"))

# Set up server
server = HTTPServer((HOST, PORT), DatabaseHTTP)
print(f"SERVER RUNNED ON {HOST}:{PORT}")
server.serve_forever()
server.server_close()
print("SERVER STOPPED :C")
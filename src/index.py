from flask import Flask
from waitress import serve
import handler

app = Flask(__name__)

@app.route("/", defaults={"path": ""}, methods=["POST", "GET"])
def main_route(path):
  return handler.handle()

if __name__ == "__main__":
  serve(app, host="0.0.0.0", port=3000)
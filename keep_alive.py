import os
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main():
  return "Your bot is alive!"

def run():
    # app.run(host="0.0.0.0", port=8080)
    port = int(os.environ.get("PORT", 17995))
    app.run(host='0.0.0.0', port=port)

def alive():
    server = Thread(target=run)
    server.start()
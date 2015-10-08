from flask import Flask, request, redirect, jsonify

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    return "hello world"
if __name__=="__main__":
    app.run(host='localhost', port=80)

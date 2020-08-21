from flask import Flask, request
import json
from solve import solve, turn
import pycuber as pc


app = Flask(__name__)


@app.route("/")
def run():
    return "<h1 style='color:blue'>Hello There!</h1>"

@app.route("/solve",methods=['POST'])
def predict():

    content = request.get_json()
    target_cube = turn(content)
    if type(target_cube) == "str":
        return json.dumps([False, "Invalid input"])
    if target_cube.is_valid() == False:
        return json.dumps([False, "Invalid input"])

    is_solved, actions = solve(target_cube)
    results = [is_solved, actions]

    return json.dumps(results)

if __name__ == "__main__":
    app.run(host='0.0.0.0')


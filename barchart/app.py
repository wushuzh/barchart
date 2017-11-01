from flask import Flask, render_template
import random


app = Flask(__name__)


@app.route("/<int:bars_count>/")
def cahrt(bars_count):
    if bars_count <= 0:
        bars_count = 1

    data = {"days": [], "bugs": [], "costs": []}
    for i in range(1, bars_count + 1):
        data['days'].append(i)
        data['bugs'].append(random.randint(1, 100))
        data['costs'].append(random.uniform(1.00, 1000.00))

    print(data)

    return render_template("chart.html", bars_count=bars_count)


if __name__ == "__main__":
    app.run(debug=True)

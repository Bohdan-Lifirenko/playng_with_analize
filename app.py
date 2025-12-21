from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

dates = pd.date_range(start="2023-01-01", periods=30, freq="D")

df = pd.DataFrame({
    "date": dates,
    "revenue": np.linspace(100, 300, 30),
    "profit": np.linspace(20, 120, 30),
    "expenses": np.linspace(80, 180, 30)
})

@app.route("/")
def index():
    return render_template(
        "index.html",
        dates=df["date"].dt.strftime("%Y-%m-%d").tolist()
    )

@app.route("/data")
def get_data():
    selected_date = request.args.get("date")

    filtered = df[df["date"] <= selected_date]

    return jsonify({
        "date": filtered["date"].astype(str).tolist(),
        "revenue": filtered["revenue"].tolist(),
        "profit": filtered["profit"].tolist(),
        "expenses": filtered["expenses"].tolist()
    })

if __name__ == "__main__":
    app.run(debug=True)
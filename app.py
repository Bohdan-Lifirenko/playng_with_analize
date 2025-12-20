from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Дані з колонкою дат
df = pd.DataFrame({
    "date": pd.date_range(start="2023-01-01", periods=30, freq="D"),
    "value": [i * 10 + (i % 5) * 7 for i in range(30)]
})

@app.route("/")
def index():
    dates = df["date"].dt.strftime("%Y-%m-%d").tolist()

    return render_template(
        "index.html",
        dates=dates
    )


@app.route("/data")
def get_data():
    selected_date = request.args.get("date")

    filtered = df[df["date"] <= selected_date]

    return jsonify({
        "date": filtered["date"].astype(str).tolist(),
        "value": filtered["value"].tolist()
    })

if __name__ == "__main__":
    app.run(debug=True)
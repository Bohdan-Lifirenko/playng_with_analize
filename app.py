from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Дані з колонкою дат
df = pd.DataFrame({
    "date": pd.date_range(start="2023-01-01", periods=30, freq="D"),
    "value": [i * 10 + (i % 5) * 7 for i in range(30)]
})

df.head()

@app.route("/")
def index():
    min_date = df["date"].min().strftime("%Y-%m-%d")
    max_date = df["date"].max().strftime("%Y-%m-%d")
    return render_template(
        "index.html",
        min_date=min_date,
        max_date=max_date
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
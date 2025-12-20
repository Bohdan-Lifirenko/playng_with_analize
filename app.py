from flask import Flask, render_template
import plotly.express as px
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    # Дані
    df = pd.DataFrame({
        "year": [2019, 2020, 2021, 2022, 2023],
        "revenue": [100, 150, 130, 180, 220]
    })

    # Графік
    fig = px.line(
        df,
        x="year",
        y="revenue",
        title="Динаміка виручки"
    )

    # Перетворення графіка в HTML
    graph_html = fig.to_html(full_html=False)

    return render_template("index.html", graph_html=graph_html)

if __name__ == "__main__":
    app.run(debug=True)
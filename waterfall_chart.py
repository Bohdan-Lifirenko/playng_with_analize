from flask import Flask, render_template
import plotly.graph_objects as go

app = Flask(__name__)

@app.route('/')
@app.route('/')
def waterfall_page():
    # Дані для прикладу (можна динамічно завантажувати з бази даних)
    assets = 100000
    liabilities = 150000
    equity = assets - liabilities  # -50000

    # Create individual bar traces instead of waterfall
    fig = go.Figure()

    # Liabilities bar (blue)
    fig.add_trace(go.Bar(
        x=["Зобов'язання (Liabilities)"],
        y=[liabilities],
        name="Зобов'язання",
        marker={"color": "#42A5F5", "line": {"color": "#1565C0", "width": 2}},
        text=[f"{liabilities:,} грн"],
        textposition="outside"
    ))

    # Equity bar (green if positive, red if negative)
    equity_color = "#4CAF50" if equity >= 0 else "#EF5350"
    equity_line_color = "#388E3C" if equity >= 0 else "#D32F2F"

    fig.add_trace(go.Bar(
        x=["Власний капітал (Equity)"],
        y=[equity],
        name="Власний капітал",
        marker={"color": equity_color, "line": {"color": equity_line_color, "width": 2}},
        text=[f"{equity:,} грн"],
        textposition="outside"
    ))

    # Assets bar (grey - keeping original color)
    fig.add_trace(go.Bar(
        x=["Активи (Assets)"],
        y=[assets],
        name="Активи",
        marker={"color": "#9E9E9E", "line": {"color": "#757575", "width": 2}},
        text=[f"{assets:,} грн"],
        textposition="outside"
    ))

    fig.update_layout(
        title={
            "text": "Баланс компанії: Активи = Зобов'язання + Власний капітал",
            "font": {"size": 20, "color": "#333333"}
        },
        xaxis_title="Компоненти балансу",
        yaxis_title="Значення (грн)",
        yaxis={"gridcolor": "#E0E0E0", "zerolinecolor": "#BDBDBD"},
        font={"size": 14},
        height=500,
        showlegend=False,
        hovermode="x unified",
        plot_bgcolor="#F5F5F5",
        paper_bgcolor="#FFFFFF",
        bargap=0.4
    )

    if equity < 0:
        fig.add_annotation(
            x="Власний капітал (Equity)",
            y=equity / 2 if equity > 0 else equity * 1.5,
            text="Негативний капітал: дефіцит<br>(може вказувати на ризики)",
            showarrow=True,
            arrowhead=1,
            font={"size": 12, "color": "#757575"},
            align="center"
        )

    # Конвертація графіка в HTML (з JS для інтерактивності)
    graph_html = fig.to_html(full_html=False, include_plotlyjs='cdn')  # Використовуємо CDN для Plotly JS

    return render_template('waterfall_page.html', graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True)
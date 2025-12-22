from flask import Flask, render_template
import plotly
import plotly.graph_objects as go
import json

app = Flask(__name__)


@app.route('/')
def ploty_index():
    # Дані для графіка
    values = [120, -80]
    labels = ['Value A', 'Value B']

    # Створюємо Plotly графік
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=labels,
        y=values,
        marker_color=['green' if v >= 0 else 'red' for v in values],
        text=values,
        textposition='auto'
    ))
    fig.update_layout(
        yaxis=dict(
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor='black'
        ),
        plot_bgcolor='white',
        margin=dict(l=40, r=40, t=40, b=40)
    )

    # Конвертуємо графік у JSON для фронтенду
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Дані компанії для прикладу
    company = {
        'name': 'Acme Corp',
        'tax_id': '12345678',
        'kved': '62.01',
        'opf_code': 'LLC',
        'katottg': '1234567',
        'region_code': '01',
        'local_code': '001'
    }

    return render_template('ploty_index.html', graphJSON=graphJSON, company=company)


if __name__ == '__main__':
    app.run(debug=True)

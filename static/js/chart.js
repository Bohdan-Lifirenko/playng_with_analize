const { company } = window.APP_CONFIG;
console.log(company.tax_id);
const taxId = company.tax_id;

// стартове завантаження (остання дата)
document.addEventListener('DOMContentLoaded', () => {
    provideDataToBalanceChart()
    provideDataToRevenueChart()
    provideDataToBalanceWFChart()
});

function provideDataToRevenueChart() {
    fetch(`/api/revenue/${taxId}`)
        .then(response => {
            data = response.json();
            console.log(data)
            return data;
        })
        .then(data => {
            // Extract dates and values
            const dates = data.map(item => item.date);
            const values = data.map(item => item.value);

            // Create Plotly chart
            const trace = {
                x: dates,
                y: values,
                type: 'scatter',
                mode: 'lines+markers',
                name: 'Revenue',
                line: {
                    color: '#667eea',
                    width: 3
                },
                marker: {
                    size: 8,
                    color: '#764ba2'
                }
            };

            const layout = {
                title: {
                    text: 'Revenue Over Time',
                    font: { size: 18 }
                },
                xaxis: {
                    title: 'Date',
                    type: 'date'
                },
                yaxis: {
                    title: 'Revenue (UAH)',
                    tickformat: ',.0f'
                },
                hovermode: 'closest',
                plot_bgcolor: '#f8f9fa',
                paper_bgcolor: 'white',
                margin: { t: 50, r: 30, b: 50, l: 80 }
            };

            const config = {
                responsive: true,
                displayModeBar: true,
                displaylogo: false,
                modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d']
            };

            Plotly.newPlot('revenueChart', [trace], layout, config);
        });
}

function provideDataToBalanceChart() {
    const selectedDate = '2024-12-31';

    fetch(`/api/balance/${taxId}?date=${selectedDate}`)
        .then(response => {
            data = response.json();
            console.log(data)
            return data;
        })
        .then(data => {
            // Create pie chart for equity and liabilities
            const trace = {
                values: [data.equity, data.liabilities],
                labels: ['Equity', 'Liabilities'],
                type: 'pie',
                marker: {
                    colors: ['#4ade80', '#f87171']
                },
                textinfo: 'label+percent+value',
                texttemplate: '%{label}<br>%{value:,.0f} UAH<br>(%{percent})',
                hovertemplate: '<b>%{label}</b><br>%{value:,.0f} UAH<br>%{percent}<extra></extra>'
            };

            const layout = {
                title: {
                    text: `Balance Sheet - ${selectedDate}`,
                    font: {size: 18}
                },
                annotations: [{
                    text: `Total Assets<br>${data.assets}`,
                    x: 0.5,
                    y: -0.15,
                    xref: 'paper',
                    yref: 'paper',
                    showarrow: false,
                    font: {size: 14, color: '#6b7280'}
                }],
                showlegend: true,
                legend: {
                    orientation: 'h',
                    y: -0.3
                },
                margin: {t: 50, r: 30, b: 100, l: 30}
            };

            const config = {
                responsive: true,
                displayModeBar: true,
                displaylogo: false,
                modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d']
            };

            Plotly.newPlot('balanceChart', [trace], layout, config);
        });
}

function provideDataToBalanceWFChart() {
    const selectedDate = '2024-12-31';
    fetch(`/api/balance/${taxId}?date=${selectedDate}`)
        .then(response =>{
            data = response.json();
            console.log(data)
            return data;
        })
        .then(data => {
            // Calculate liabilities from the balance equation: Assets = Liabilities + Equity
            const assets = data.assets;
            const equity = data.equity;
            const liabilities = assets - equity;

            // Create waterfall chart data
            const trace = {
                type: 'waterfall',
                orientation: 'v',
                measure: ['relative', 'relative', 'total'],
                x: ['Equity', 'Liabilities', 'Total Assets'],
                textposition: 'outside',
                text: [
                    `${equity.toLocaleString()} UAH`,
                    `${liabilities.toLocaleString()} UAH`,
                    `${assets.toLocaleString()} UAH`
                ],
                y: [equity, liabilities, 0], // 0 for total since it's calculated automatically
                connector: {
                    line: {
                        color: "rgb(63, 63, 63)"
                    }
                },
                increasing: {
                    marker: {
                        color: equity >= 0 ? '#4ade80' : '#f87171' // Green for positive equity, red for negative
                    }
                },
                decreasing: {
                    marker: {
                        color: '#f87171' // Red for liabilities (debt)
                    }
                },
                totals: {
                    marker: {
                        color: '#6b7280' // Gray for total assets
                    }
                },
                hovertemplate: '<b>%{x}</b><br>%{y:,.0f} UAH<extra></extra>'
            };

            const layout = {
                title: {
                    text: `Balance Sheet Waterfall - ${selectedDate}`,
                    font: { size: 18 }
                },
                xaxis: {
                    title: 'Balance Components'
                },
                yaxis: {
                    title: 'Amount (UAH)',
                    tickformat: ',.0f'
                },
                annotations: [
                    {
                        text: `Balance Equation: Assets = Liabilities + Equity<br>` +
                              `${assets.toLocaleString()} = ${liabilities.toLocaleString()} + ${equity.toLocaleString()}`,
                        x: 0.5,
                        y: 1.1,
                        xref: 'paper',
                        yref: 'paper',
                        showarrow: false,
                        font: { size: 12, color: '#6b7280' },
                        align: 'center'
                    }
                ],
                showlegend: false,
                plot_bgcolor: '#f8f9fa',
                paper_bgcolor: 'white',
                margin: { t: 80, r: 30, b: 50, l: 80 }
            };

            const config = {
                responsive: true,
                displayModeBar: true,
                displaylogo: false,
                modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d']
            };

            Plotly.newPlot('balanceWFChart', [trace], layout, config);
        })
        .catch(error => {
            console.error('Error fetching balance data:', error);
        });
}

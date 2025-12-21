const dates = window.APP_CONFIG.dates;
const select = document.getElementById("dateSelect");

// dropdown
dates.forEach(date => {
    const option = document.createElement("option");
    option.value = date;
    option.textContent = date;
    select.appendChild(option);
});

function updateCharts(selectedDate) {
    fetch(`/data?date=${selectedDate}`)
        .then(res => res.json())
        .then(data => {

            Plotly.react("chartRevenue", [{
                x: data.date,
                y: data.revenue,
                type: "scatter",
                mode: "lines+markers"
            }], {
                title: "Виручка"
            });

            Plotly.react("chartProfit", [{
                x: data.date,
                y: data.profit,
                type: "scatter",
                mode: "lines+markers"
            }], {
                title: "Прибуток"
            });

            Plotly.react("chartExpenses", [{
                x: data.date,
                y: data.expenses,
                type: "scatter",
                mode: "lines+markers"
            }], {
                title: "Витрати"
            });

        });
}

select.addEventListener("change", () => {
    updateCharts(select.value);
});

// стартове завантаження (остання дата)
select.value = dates[dates.length - 1];
updateCharts(select.value);

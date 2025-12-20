const dateSelect = document.getElementById("dateSelect");
const dates = window.APP_CONFIG.dates;

// Заповнення випадаючого списку
dates.forEach(date => {
    const option = document.createElement("option");
    option.value = date;
    option.textContent = date;
    dateSelect.appendChild(option);
});

function loadData(selectedDate) {
    fetch(`/data?date=${selectedDate}`)
        .then(response => response.json())
        .then(data => {
            Plotly.react(
                "chart",
                [{
                    x: data.date,
                    y: data.value,
                    type: "scatter",
                    mode: "lines+markers"
                }],
                {
                    title: `Динаміка значень до ${selectedDate}`,
                    xaxis: { title: "Дата" },
                    yaxis: { title: "Значення" }
                }
            );
        });
}

// Обробник зміни дати
dateSelect.addEventListener("change", () => {
    loadData(dateSelect.value);
});

// Початковий рендер (остання дата)
dateSelect.value = dates[dates.length - 1];
loadData(dateSelect.value);

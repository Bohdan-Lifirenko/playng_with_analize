const minDate = new Date(window.APP_CONFIG.minDate);
const maxDate = new Date(window.APP_CONFIG.maxDate);

const slider = document.getElementById("dateSlider");
const label = document.getElementById("dateLabel");

const daysCount = Math.round(
    (maxDate - minDate) / (1000 * 60 * 60 * 24)
);

slider.min = 0;
slider.max = daysCount;
slider.value = 0;

function formatDate(date) {
    return date.toISOString().split("T")[0];
}

function loadData(daysOffset) {
    const selectedDate = new Date(minDate);
    selectedDate.setDate(selectedDate.getDate() + Number(daysOffset));

    const dateStr = formatDate(selectedDate);
    label.textContent = dateStr;

    fetch(`/data?date=${dateStr}`)
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
                    title: "Динаміка значення до вибраної дати",
                    xaxis: { title: "Дата" },
                    yaxis: { title: "Значення" }
                }
            );
        });
}

slider.addEventListener("input", () => {
    loadData(slider.value);
});

// Початкове завантаження
loadData(0);

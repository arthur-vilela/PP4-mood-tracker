document.addEventListener("DOMContentLoaded", function () {
    fetch("/dashboard/mood-calendar/")
        .then((response) => response.json())
        .then((data) => {
            const moods = ["Happy", "Sad", "Anxious", "Angry", "Excited", "Calm", "Tired"];
            const colors = d3
                .scaleOrdinal()
                .domain(moods)
                .range(["#FFD700", "#FF4500", "#9370DB", "#FF6347", "#32CD32", "#87CEEB", "#A9A9A9"]);

            document.querySelectorAll(".calendar-div").forEach((container) => {
                const monthId = container.id.split("-")[1];
                const year = parseInt(monthId.slice(0, 4), 10);
                const month = parseInt(monthId.slice(4, 6), 10) - 1;

                const containerWidth = container.offsetWidth; // Get the parent container width
                const cellSize = Math.min(containerWidth / 53, 17); // Adjust cell size based on available width

                const svg = d3
                    .select(`#${container.id}`)
                    .append("svg")
                    .attr("width", containerWidth) // Set the width to the container's width
                    .attr("height", cellSize * 7 + 20) // Height adjusts based on cell size
                    .append("g")
                    .attr("transform", `translate(${(containerWidth - cellSize * 53) / 2}, 20)`); // Center the grid

                const firstDayOfMonth = new Date(year, month, 1);

                svg.selectAll(".day")
                    .data(d3.timeDays(firstDayOfMonth, d3.timeMonth.offset(firstDayOfMonth, 1)))
                    .enter()
                    .append("rect")
                    .attr("width", cellSize)
                    .attr("height", cellSize)
                    .attr("x", (d) => d3.timeWeek.count(d3.timeYear(d), d) * cellSize)
                    .attr("y", (d) => d.getDay() * cellSize)
                    .style("fill", (d) => (data[d3.timeFormat("%Y-%m-%d")(d)] ? colors(data[d3.timeFormat("%Y-%m-%d")(d)]) : "#EEE"))
                    .style("stroke", "#CCC");
            });
        });
});

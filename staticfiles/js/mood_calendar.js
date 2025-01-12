document.addEventListener("DOMContentLoaded", function () {
    fetch("/dashboard/mood-calendar/")
        .then((response) => {
            const contentType = response.headers.get("content-type");
            if (response.ok && contentType && contentType.includes("application/json")) {
                return response.json();
            } else {
                throw new Error("Unexpected response. Likely unauthenticated or an error occurred.");
            }
        })
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

                const containerWidth = container.offsetWidth;
                const minCellSize = 20; // Define a minimum cell size
                const maxCellSize = 35; // Define a maximum cell size
                const cellSize = Math.max(minCellSize, Math.min(containerWidth / 30, maxCellSize)); // Ensure cell size remains in bounds

                const svg = d3
                    .select(`#${container.id}`)
                    .append("svg");

                const g = svg
                    .append("g");

                const firstDayOfMonth = new Date(year, month, 1);
                const days = d3.timeDays(firstDayOfMonth, d3.timeMonth.offset(firstDayOfMonth, 1));

                // Add squares (rect elements)
                g.selectAll(".day")
                    .data(days)
                    .enter()
                    .append("rect")
                    .attr("width", cellSize)
                    .attr("height", cellSize)
                    .attr("x", (d) => {
                        const startOfMonth = d3.timeMonth(d);
                        return d3.timeWeek.count(startOfMonth, d) * cellSize;
                    })
                    .attr("y", (d) => d.getDay() * cellSize)
                    .style("fill", (d) => {
                        const dateStr = d3.timeFormat("%Y-%m-%d")(d);
                        return data[dateStr] ? colors(data[dateStr]) : "#EEE";
                    })
                    .style("stroke", "#CCC");

                // Add day numbers (text elements)
                g.selectAll(".day-number")
                    .data(days)
                    .enter()
                    .append("text")
                    .attr("x", (d) => {
                        const startOfMonth = d3.timeMonth(d);
                        return d3.timeWeek.count(startOfMonth, d) * cellSize + cellSize / 2;
                    })
                    .attr("y", (d) => d.getDay() * cellSize + cellSize / 1.5)
                    .attr("text-anchor", "middle")
                    .attr("font-size", `${cellSize / 3}px`)
                    .attr("fill", "#000")
                    .text((d) => d.getDate());

                // Dynamically adjust the <svg> size
                const bbox = g.node().getBBox();
                svg
                    .attr("width", bbox.width + 2 * cellSize)
                    .attr("height", bbox.height + 2 * cellSize);

                // Center the <g> element within the <svg>
                g.attr(
                    "transform",
                    `translate(${(svg.attr("width") - bbox.width) / 2}, ${(svg.attr("height") - bbox.height) / 2})`
                );
            });
        });
});

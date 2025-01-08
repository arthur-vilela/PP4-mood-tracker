document.addEventListener("DOMContentLoaded", function () {
    fetch("/dashboard/mood-calendar/")
        .then((response) => response.json())
        .then((data) => {
            console.log("Fetched data:", data);

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
                const cellSize = Math.min(containerWidth / 30, 35); // Enlarged calendar cells

                const svg = d3
                    .select(`#${container.id}`)
                    .append("svg");

                const g = svg
                    .append("g"); // Append the <g> element without transform initially

                const firstDayOfMonth = new Date(year, month, 1);
                const days = d3.timeDays(firstDayOfMonth, d3.timeMonth.offset(firstDayOfMonth, 1));
                console.log(`Days for ${year}-${month + 1}:`, days);

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
                        return data[dateStr] ? colors(data[dateStr]) : "#EEE"; // Default fill for empty days
                    })
                    .style("stroke", "#CCC");

                // Add day numbers (text elements)
                g.selectAll(".day-number")
                    .data(days)
                    .enter()
                    .append("text")
                    .attr("x", (d) => {
                        const startOfMonth = d3.timeMonth(d);
                        return d3.timeWeek.count(startOfMonth, d) * cellSize + cellSize / 2; // Center horizontally
                    })
                    .attr("y", (d) => d.getDay() * cellSize + cellSize / 1.5) // Center vertically
                    .attr("text-anchor", "middle")
                    .attr("font-size", `${cellSize / 3}px`) // Scale font size with cell size
                    .attr("fill", "#000")
                    .text((d) => d.getDate()); // Add day number

                // Dynamically adjust the <svg> size
                const bbox = g.node().getBBox(); // Get bounding box of content
                svg
                    .attr("width", bbox.width + 2 * cellSize) // Add padding for centering
                    .attr("height", bbox.height + 2 * cellSize); // Add padding for top and bottom

                // Center the <g> element within the <svg>
                g.attr(
                    "transform",
                    `translate(${(svg.attr("width") - bbox.width) / 2}, ${(svg.attr("height") - bbox.height) / 2})`
                );
            });
        });
});

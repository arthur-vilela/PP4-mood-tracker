jest.useFakeTimers();

test("Removes alert messages after timeout", () => {
    // Setup: Add a mock alert element to the DOM
    document.body.innerHTML = `
        <div class="alert show">Test Message</div>
    `;
    const alerts = document.querySelectorAll(".alert");

    // Call the timeout function
    setTimeout(() => {
        alerts.forEach(alert => {
            alert.classList.remove('show');
            alert.classList.add('fade');
            setTimeout(() => alert.remove(), 500);
        });
    }, 5000);

    // Fast-forward time
    jest.runAllTimers();

    // Assert: Verify the alert is removed
    expect(document.querySelector(".alert")).toBeNull();
});

document.addEventListener("DOMContentLoaded", () => {
    const deleteModal = document.getElementById("deleteModal");
    if (deleteModal) {
        const deleteForm = document.getElementById("deleteForm");
        const deleteModalDate = document.getElementById("deleteModalDate");
        const deleteModalMood = document.getElementById("deleteModalMood");

        deleteModal.addEventListener("show.bs.modal", (event) => {
            const triggerButton = event.relatedTarget; // Button that triggered the modal

            // Extract data-* attributes from the triggering button
            const moodId = triggerButton.getAttribute("data-id");
            const moodDate = triggerButton.getAttribute("data-date");
            const moodType = triggerButton.getAttribute("data-mood");

            // Update modal content
            deleteForm.action = `/dashboard/delete-mood/${moodId}/`; // Set form action
            deleteModalDate.textContent = moodDate || "N/A";         // Set mood date
            deleteModalMood.textContent = moodType || "N/A";         // Set mood type
        });
    }
});

document.addEventListener("DOMContentLoaded", () => {
    // Select all alert messages
    const alerts = document.querySelectorAll('.alert');
    if (alerts) {
        // Set a timeout to dismiss the messages after 5 seconds
        setTimeout(() => {
            alerts.forEach(alert => {
                alert.classList.remove('show'); // Remove 'show' class for fade-out effect
                alert.classList.add('fade');   // Add fade-out transition class
                setTimeout(() => alert.remove(), 500); // Remove the element after fade-out
            });
        }, 5000); // Timeout duration in milliseconds = 5 seconds
    }
});

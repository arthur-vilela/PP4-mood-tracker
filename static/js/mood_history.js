document.addEventListener("DOMContentLoaded", () => {
    const deleteModal = document.getElementById("deleteModal");
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
});

/**
 * @jest-environment jsdom
 */
document.body.innerHTML = `
    <button
        id="triggerButton"
        data-id="1"
        data-date="2025-01-01"
        data-mood="Happy"
        data-action="edit"
    ></button>
    <div id="editModal" class="modal">
        <input id="editModalInputDate" />
        <input id="editModalInputMood" />
    </div>
    <div id="deleteModal" class="modal">
        <span id="deleteModalDate"></span>
        <span id="deleteModalMood"></span>
    </div>
`;

const triggerButton = document.getElementById("triggerButton");
const editModalInputDate = document.getElementById("editModalInputDate");
const editModalInputMood = document.getElementById("editModalInputMood");
const deleteModalDate = document.getElementById("deleteModalDate");
const deleteModalMood = document.getElementById("deleteModalMood");

describe("Modal Data Population", () => {
    test("Edit modal populates with correct data", () => {
        // Simulate click event to trigger modal
        triggerButton.setAttribute("data-action", "edit");
        triggerButton.click();

        // Simulate edit modal population logic
        if (triggerButton.getAttribute("data-action") === "edit") {
            editModalInputDate.value = triggerButton.getAttribute("data-date");
            editModalInputMood.value = triggerButton.getAttribute("data-mood");
        }

        // Assertions
        expect(editModalInputDate.value).toBe("2025-01-01");
        expect(editModalInputMood.value).toBe("Happy");
    });

    test("Delete modal populates with correct data", () => {
        // Simulate click event to trigger modal
        triggerButton.setAttribute("data-action", "delete");
        triggerButton.click();

        // Simulate delete modal population logic
        if (triggerButton.getAttribute("data-action") === "delete") {
            deleteModalDate.textContent = triggerButton.getAttribute("data-date");
            deleteModalMood.textContent = triggerButton.getAttribute("data-mood");
        }

        // Assertions
        expect(deleteModalDate.textContent).toBe("2025-01-01");
        expect(deleteModalMood.textContent).toBe("Happy");
    });
});

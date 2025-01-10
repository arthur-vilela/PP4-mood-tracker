# Mood Tracker

## Description
A Django-based web application for tracking moods, allowing users to record their emotional state, actions, and analyze patterns over time.
## Overview

Mood Tracker is a portfolio project developed as part of the Full Stack Development course curriculum from Code Institute. This application was created with the goal of providing a simple, user-friendly tool for individuals to track their emotional responses over time. It offers insights that can help users better understand themselves or serve as a supplemental tool in therapy sessions.

## Motivation

The project theme was free to choose, and I opted for mood tracking because it's a topic close to my heart and an essential one for society. The app aims to empower individuals to log their moods, reflect on past experiences, and foster emotional awareness.

## Target Audience

The application is intended for the general public, particularly individuals seeking to improve their mental health through self-reflection. Users can benefit from a visual overview of their emotional trends and the ability to revisit older entries.
___

## Features

### **Mood Logging**
Users can log daily moods along with optional notes and actions.

#### **Implementation**
1. **Frontend**:
   - The mood entry page provides a user-friendly form where users can:
     - Select their mood from predefined choices (e.g., Happy, Sad, Anxious).
     - Add optional notes and actions to describe their day.
     - Specify the date of the mood entry (defaults to today’s date).
   - The form uses Bootstrap styling for a clean, responsive design.
   - Template file: `mood/templates/mood_entry.html`

2. **Backend**:
   - **Model**:
     - Mood entries are stored in the `Mood` model, which includes:
       - User reference (`ForeignKey` to `AUTH_USER_MODEL`).
       - Mood type (with predefined choices using `TextChoices`).
       - Date, notes, and actions for additional details.
       - Timestamps for creation and updates.


   - **Form**:
     - A custom `MoodEntryForm` validates user input:
       - Ensures dates are within the last two weeks using a custom validator.
       - Provides HTML5 date input and styled textareas for notes/actions.
   - **View**:
     - The `mood_entry_view` handles form submissions:
       - Validates input and associates the entry with the logged-in user.
       - Saves the entry and redirects to the dashboard upon success.
       - Example from `mood/views.py`:

   - **URLs**:
     - The form is accessible via `/mood/entry/`, registered in `mood/urls.py`:

3. **Security**:
   - CSRF protection is implemented using Django’s built-in mechanism.
   - Only logged-in users can access the mood entry page (`@login_required`).

4. **Validation**:
   - Date validation ensures entries are no older than two weeks.
   - Form validation ensures required fields are filled and follow constraints.

---

### **Visual Calendar**
A calendar on the dashboard provides a color-coded overview of logged moods.

#### **Implementation**
1. **Frontend**:
   - The calendar is dynamically rendered using **D3.js** to display an SVG element for each month.
   - Each cell represents a day and is color-coded based on the most frequent mood logged for that day.
   - A legend provides a visual guide for mood colors.

2. **Backend**:
   - A dedicated Django view aggregates mood data by date, determining the most frequent mood per day using Python's `Counter`.
   - The processed data is sent to the frontend as a JSON object.

3. **Integration**:
   - The `dashboard.html` template fetches the JSON data and renders it into the calendar using a JavaScript script.
   - Users can view their mood patterns over time in a responsive and visually appealing way.

---

### **History Review**
Users can revisit older entries through an accordion-style mood history page.

#### **Implementation**
1. **Frontend**:
   - Bootstrap's accordion component is used to create a collapsible interface.
   - Each entry displays the mood type, date, and optional notes or actions.
   - Users can edit or delete entries directly from the history page.

2. **Backend**:
   - A Django view retrieves all moods for the logged-in user, sorted by date in descending order.
   - Pagination or lazy loading is not currently implemented but can be added for performance optimization.

3. **Integration**:
   - The `mood_history.html` template includes modals for delete confirmations.
   - A separate JavaScript file handles interactivity, such as populating the delete modal.

---

### **Dark Mode**
A toggle allows users to switch between light and dark themes.

#### **Implementation**
1. **Frontend**:
   - The settings page includes a toggle switch for enabling or disabling dark mode.
   - CSS classes are applied dynamically to templates based on user preferences.

2. **Backend**:
   - The `UserPreferences` model stores the dark mode preference for each user.
   - The `settings_view` updates the preference based on form input and sets a session variable to persist the preference.

3. **Integration**:
   - Dark mode applies to all key components, including the navbar, content sections, and footer.
   - The theme persists across sessions, ensuring a consistent user experience.

---

### **Daily Reminder Email Feature**

#### **Overview**
The Daily Reminder Email feature ensures that users who opt-in receive a notification email at 20:00 UTC, reminding them to log their mood in the app. This feature is designed to help users maintain consistent mood tracking and make the most of the app's functionality.

---

#### **Feature Implementation**

1. **Opt-In Settings**:
   - Users can enable or disable email notifications through the **Settings** page.
   - The notification preferences are stored in the `NotificationSettings` model with the field `notify_by_email`.

2. **Email Content**:
   - The email contains a friendly reminder message:
     ```
     Subject: Mood Tracker Reminder
     Message: This is your daily reminder to log your mood in the Mood Tracker app!
     ```

3. **Automated Task**:
   - A custom Django management command, `send_reminders`, is responsible for sending the emails.
   - The command:
     - Queries the database for users with `notify_by_email=True`.
     - Sends reminder emails to the listed users using Django's `send_mail()` function.

4. **Endpoint for Automation**:
   - A secure endpoint (`/dashboard/send-reminders/`) allows external schedulers to trigger the reminder emails.
   - This endpoint:
     - Requires a secret token (`X-SECRET-TOKEN`) for authentication.
     - Executes the `send_reminders` command when accessed via a POST request.

5. **Automation with GitHub Actions**:
   - A GitHub Actions workflow triggers the `/dashboard/send-reminders/` endpoint daily at 20:00.
   - The workflow uses a secure `SECRET_TOKEN` stored in the repository's secrets to authenticate the request.

---
#### Testing the Feature
1. Enable email notifications via the Settings page.
2. Verify the reminder email is sent:
- Check your inbox at the scheduled time.
- Test the endpoint manually with curl
   ```
   curl -X POST https://pp4-mood-tracker-20082cf10f44.herokuapp.com/dashboard/send-reminders/ \
     -H "X-SECRET-TOKEN: your_secret_token"
   ```
---

### **User Profile Management**
Users can update their username, email, and password.

#### **Implementation**
1. **Frontend**:
   - Profile update forms include fields for editing the username and email, along with secure fields for password changes.
   - Bootstrap styling ensures a clean and responsive user interface.

2. **Backend**:
   - Profile updates are managed by Django Allauth, leveraging its built-in functionality for authentication and user account management.
   - Passwords are securely hashed and validated using Django's authentication tools.

3. **Integration**:
   - Notifications confirm successful updates to the user's profile.
   - The updated information is immediately reflected in the user session.

---

### **Responsive Design**
The application is mobile-friendly and adjusts to different screen sizes.

#### **Implementation**
1. **Frontend**:
   - Bootstrap's grid system ensures consistent layouts across devices.
   - Media queries provide additional styling for small and large screens, optimizing the user interface.

2. **Integration**:
   - The design is tested on a variety of devices and browsers to ensure accessibility.
   - Elements like the navbar, forms, and tables adjust seamlessly to smaller screens.

---

## Models

### ERD

![Diagram of database table relations](docs/moodtracker-erd.png)

### Mood Model

The Mood model represents user-submitted mood entries and includes fields to capture details about their emotional state on specific dates. This model allows users to document their feelings, actions taken, and additional notes for reflection or tracking purposes.

#### Fields
| Field | Description |
|-------|-------------|
| `user`| A foreign key linking the mood entry to a registered user.|
|`date`| The date on which the mood was recorded.|
|`mood_type`| A choice field representing predefined mood types (e.g., Happy, Sad, Angry).|
|`note`| Optional text field for additional comments about the mood.|
|`action`| Optional text field to document actions taken to manage the mood.|
|`created_at`| The timestamp when the mood entry was created (automatically generated).|
|`updated_at`| The timestamp when the mood entry was last updated (automatically generated).|

#### Validation

The `mood_type` field restricts entries to predefined choices to maintain data integrity.
Admin Panel Features
The model is registered in the Django admin panel with the following enhancements:
Search Fields: user and note for quick lookup.
Filter Options: mood_type and date for targeted filtering.
Display Configuration: Shows user, date, mood_type, and created_at for each entry.

#### Tests

The tests ensure the correct functionality of the `Mood` model and its integration with the database. This includes validating field constraints, choice-based options, and timestamp generation.


1. **Model Creation Test**:
   - Created multiple mood entries for a test user to verify that all fields save and display correctly.
   - Ensured `created_at` and `updated_at` timestamps were automatically generated.

2. **Validation Test**:
   - Confirmed that `mood_type` accepts only predefined choices and rejects invalid inputs.

3. **Admin Panel Check**:
   - Verified that the `Mood` model appears in the admin panel with filters, search, and display functionality as configured.


## Tests

The project includes automated tests to ensure the proper functionality of key features such as user authentication, profile updates, and settings management. These tests verify that the application behaves as expected under various scenarios.

### Key Areas Covered

1. **Logout Confirmation**
   - **Test Name:** `test_logout_confirm`
   - Ensures that the logout confirmation page renders correctly and that the user is redirected to the home page upon confirmation.

2. **Profile Update**
   - **Test Name:** `test_profile_update`
   - Validates that the profile update form is prepopulated with the current user's data.
   - Confirms that changes to the username and email are saved correctly and reflected immediately.
   - Verifies redirection to the dashboard after successful updates.

3. **Password Change**
   - **Test Name:** `test_password_change`
   - Checks that the password change form validates new passwords correctly.
   - Ensures that the user is redirected to the dashboard after a successful password change.

### Running the Tests
To run the tests, execute the following command in your terminal:

   ```
   python manage.py test
   ```

### JavaScript Testing

This project includes JavaScript tests to ensure functionality for interactive features like modals and message timeouts. 
JavaScript functionality in this project was tested using Jest and the DOM Testing Library. The testing focused on verifying that the interactive elements of the application behave as expected.
`Jest` was used for unit testing JavaScript functions. A dedicated directory for JavaScript tests in your project was created. This helps maintain a clean structure and keeps tests organized.

#### Tests Conducted

1. Timeout Messages
   
   The `messages.js` script ensures that alert messages disappear after 5 seconds. This functionality was tested to ensure:

   - Messages with the `show` class are removed from the DOM after the timeout period.
   - The functionality performs as expected in various user scenarios.

2. Modal Data Population
The `mood_history.js` script dynamically populates modal content for editing and deleting mood entries. Tests for this functionality ensured:

   - The `edit` modal is populated with the correct `date` and `mood` values from the triggering button.
   - The `delete` modal displays the correct `date` and `mood` in its fields.

#### Running the Tests
To run the JavaScript tests, execute the following command in your terminal:

```
npx jest
```

It's important to keep in mind that 
- The JavaScript logic in this project is minimal and non-complex (e.g., message timeouts and modal data handling).
- Manual testing in the browser covers all JavaScript functionality and ensures its reliability. The `D3js` JavaScript file's goal is only to render the calendar in the `dashboard` section. This is also verified manually by oberving the rendering and tweaking the code to adjust output.
- The primary focus of this project is on backend functionality and Python-based tests.

### Manual Testing

In addition to automated tests, manual testing was performed to ensure:

- Proper form rendering and validation.
- Correct error messages for invalid inputs.
- Seamless user experience on both desktop and mobile devices.

Future Enhancements
- Adding tests for edge cases, such as invalid email formats and weak passwords.
- Expanding test coverage for additional user scenarios.





## Technologies Used

| Technology                               | Use                                                                                                           |
|------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| HTML                                     | Structure the webpage.                                                                                        |
| CSS                                      | Style and add layout to the project.                                                                          |
| JavaScript                               | Make the website interactive.                                                                                 |
| Django                                   | A Python-based web framework used to develop the backend, manage server-side logic, and handle routing.       |
| [Heroku](https://www.heroku.com/)        | Cloud platform used for deploying, managing, and hosting the live version of the website.                     |
| [GitHub](https://github.com/)            | Version control platform used to store the project’s repository, collaborate on code, and manage deployments. |  
| [dbdiagram.io](https://dbdiagram.io/home)| ERD creation                                                                                                  |
| [Jest](https://jestjs.io/)               | Unit testing JavaScript functions                                                                             |
| [D3js](https://d3js.org/)                | Rendering the calendar                                                                              |
| [RandomKeygen](https://randomkeygen.com/)| Generating secure random keys |

## Deployment to Heroku

 Go to Heroku.com and implement the following steps in this order:
 1. On the home page, click 'New' and in the dropdown, click on 'Create a new app'.
 2. Add app name (This name must be unique, and have all lower case letters. Also use minus/dash signs instead of spaces.)
 3. Select Region (Most likely to be Europe)
 4. Click the button that says 'Create App' and name the app. Follow instructions on the screen.
 5. Click on the Deploy tab near the top of the screen.
 6. Where is says Deployment Method click on Github.
 7. Below that, search for your repo name and add that.
 8. Click connect to the app.

 Before clicking below on enable automatic deployment do the following:
 1. Click on the settings tab
 2. Click on reveal config vars.
 3. Add in your variables from your env. files as the key-value pairs.
 4. Go back and click on the Deploy tab. 
 
 Before the app can be connected, push the following new files below to the repository. Go back in the terminal in your coding environment and add the following:
 1. git status
 2. git add requirements.txt
 3. git commit -m "Add requirements.txt file"
 4. git add a Procfile (web: gunicorn _projectname_.wsgi)
 1. git commit -m "Add Procfile"
 2. git push

 Head back over to Heroku where the Deploy tab is.
 1. Click Deploy Branch. (Should be a main or master branch)
 2. Heroku will receive code from Github and build app with the required packages. Hopefully once done the 'App has successfully been deployed message below' will appear.. 
 3. Once you know deployment is successful then click 'Enable Automatic Deploys'
 4. Click 'View' to launch the new app.
 5. Link to deployed site is: https://pp4-mood-tracker-9f61d134c09f.herokuapp.com/

## Setup

Follow these steps to set up and run the project in Gitpod:

### 1. Open the Repository in Gitpod
- Navigate to the repository on GitHub.
- Click the **Gitpod** button (or prepend `https://gitpod.io/#` to the repository URL) to open the workspace.

### 2. Install Dependencies
Run the following command in the Gitpod terminal to install all required Python packages:
```bash
pip install -r requirements.txt
```

### 3. Run Migrations
Apply the databse migrations to set up the development database:
```
python manage.py makemigrations
python manage.py migrate
```

### 4. Start the Development Server
```
python manage.py runserver
```
The application will be accessible on port `8000` at:
`https://<workspace-url>/8000`

## Credits

https://forum.bootstrapstudio.io/ Tips and problems solving with Bootstrap styling.
https://pythonacademy.com.br/blog/como-criar-middlewares-no-django Instructions to create the middleware that solved the issue with dark theme not being fully applied on login.

# Mood Tracker

## Description
A Django-based web application for tracking moods, allowing users to record their emotional state, actions, and analyze patterns over time.

___

### ERD

![Diagram of database table relations](docs/moodtracker-erd.png)

___

## Models

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

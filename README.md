# UserManagmentSystem
Simple User Management System Using Python/Django 
This repository contains a simple user management project built with Python and Django. The project includes CRUD (Create, Read, Update, Delete) routes for managing user data.

Getting Started
Follow these instructions to download, set up, and run the project on your local system.

Prerequisites
1. Python (>= version 3.7)
2. pip (Python package installer)

Installation:
1. Make a project directory on your local and go inside it:
        1. mkdir <dir_name>
        2. cd <dir_name>

3. Clone the repository to your local machine using the following command:
  git clone <repository_url>

4. Create a virtual environment to isolate project dependencies:
  python3 -m venv virtual

5. Activate the virtual environment:

	1. On Windows:
			.\env\Scripts\activate
	2. On macOS and Linux:
		source env/bin/activate

6. Install project dependencies from the requirements.txt file:
  pip install -r requirements.txt

Running the Project:
1. Navigate to the driver app directory:
        1. cd userManagementSystem
        2. cd user_management_system

3. After installing the dependencies, migrate the database using the following command:( if the sqlite db does not have the table, by default it is already present )
        1. python3 manage.py makemigrations
        2. python3 manage.py migrate

4. (Optional) Import initial data into the database from input_data.json:
  python3 manage.py import_data input_data.json

5. Start the development server:
  python3 manage.py runserver

6. Open your web browser and navigate to http://127.0.0.1:8000/ to access the user management application.

Contributing:
If you'd like to contribute to this project, please follow these guidelines:

Fork the repository on GitHub.
Create a new branch with a descriptive name (git checkout -b feature/my-new-feature).
Make your changes and commit them with a clear message (git commit -am 'Add new feature').
Push your changes to your fork (git push origin feature/my-new-feature).
Submit a pull request with your changes for review.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgements
Thank you for using the User Management Project! If you have any questions or feedback, feel free to reach out.

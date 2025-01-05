# Form Builder Application

A web application for creating customizable forms, collecting anonymous responses, and viewing detailed analytics. The app allows admins to design and manage forms, add various types of questions, and analyze response data. End users can anonymously submit their responses.

## Features

### Admin Features:
- **Create and manage forms**: Admins can easily create new forms and manage existing ones.
- **Add question types**: Admins can add various types of questions, including:
  - Text
  - Dropdown
  - Checkbox

- **View Analytics**: Detailed analytics of form submissions, including response summaries and trends.

### End User Features:
- **Anonymous submissions**: Users can submit form responses anonymously without creating an account.
- **Intuitive form submission**: A simple interface for end users to fill out forms.

## Tech Stack
- **Backend**: Django (App Name: morpheus)
- **Database**: SQlite
- **Libraries/Frameworks**: 
  - Django Rest Framework

## Installation

### Prerequisites:
- Python 3.x (for backend)
- Django
- PostgreSQL (or your preferred database)

## Steps to Run

**Clone the repository**:
```bash
git clone https://github.com/ictorv/Former.git
cd Former
```
**Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  
# On Windows'venv\Scripts\activate'
```

**Install Requirements**
```bash
pip install -r requirements.txt
```

**Migration**
```bash
python manage.py makemigrations
python manage.py migrate
```

**Create Super Admin**
```bash
python manage.py createsuperuser
```

**For Running**
```bash
python manage.py runserver
```
>This will start the Django application on http://localhost:8000

___

### Key Requirements and Related Views
![requirements](Screenshots\Diagram.png)

***
### API Views
![APIs](Screenshots\apis.png)

### Form Creation And List
![list](Screenshots\form.png)

### Questions
![qn1](Screenshots\question1.png)
![qn2](Screenshots\question2.png)

### Responses List
![res](Screenshots\sub.png)

## API Testing
To run the tests, simply execute the following command:
```bash
pytest
```

### Tests
1. The ``test_admin_survey`` test checks if an admin user can get a list of surveys. It makes sure that the created survey appears in the response with a successful status. 

2. The ``test_analytics`` test checks if an authenticated admin user can retrieve the analytics for a specific survey.

3. The ``test_question`` tests the creation and retrieval of survey questions.

   + Creating a question: Tests if a simple text question can be created successfully.
   + Creating a checkbox question: Tests if a checkbox question with options can be created successfully.
   + Getting a list of questions: Tests if the list of questions can be retrieved correctly, verifying that the created questions appear.
  
4. The ``test_submissions`` tests creating a survey submission.

   + Create a submission: It checks if a submission with an answer can be successfully created for a survey.
   + Clean up: After the test, it deletes all the test data to avoid affecting other tests.

5. The ``test_survey`` tests actions related to surveys:

    + Create Survey: Checks if a new survey can be created.
    + Get Survey List: Verifies that a list of surveys can be retrieved.
    + Get Survey Details: Checks if the details of a specific survey can be fetched.
    + Duplicate Survey: Verifies that an existing survey can be duplicated.
  
### Result 

![testapi](Screenshots\test.png)
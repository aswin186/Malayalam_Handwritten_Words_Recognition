# Malayalam Handwritten Words Recognition
This project aims to recognize and convert handwritten Malayalam words from image documents into editable text. Built using machine learning and computer vision techniques, it allows for easy extraction of handwritten Malayalam text, facilitating applications in document digitization, data extraction, and more.

## Features
- Recognizes Malayalam handwritten characters and words from images.
- Converts recognized text to an editable digital format.

## Getting Started

### Prerequisites
To clone and run this project locally, you need to have [Python 3] (https://www.python.org/) installed.

### Cloning the Repository
git clone https://github.com/aswin186/Malayalam_Handwritten_Words_Recognition.git

### Create a virtual environment
python -m venv env

### Activate the virtual environment
.\env\Scripts\activate

### Change the Directory to
cd Malayalam_Handwritten_Words_Recognition/hcr

### Install the required dependencies
pip install -r requirements.txt

### Database Migrations
Once dependencies are installed, apply the database migrations
python manage.py migrate

### Running the Development Server
To start the Django development server, run
python manage.py runserver

### Now, you can access the project at http://127.0.0.1:8000/ in your browser.

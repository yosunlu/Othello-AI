# OthelloML

BACKEND FOLDER

## Getting started

### Configuring for running locally (Windows)

**Use Git Bash. You must have Python installed on your machine and added to your system path**
Open Git Bash in the root directory of the project (NOT the /Backend folder!). Have Visual Studio Code open in the background.

Run `python -m venv .venv`

Run `source .venv/Scripts/Activate`

Visual Studio Code should be displaying some popup about a virtual environment. Click the button that tells VSC to do whatever it wants (I don't recall exactly what it says, but just agree).

Run `pip install -r Backend/requirements.txt`

Now you have created a virtual Python environment and installed all of the required components.

`cd Backend` into the Backend folder and run `python app.py` to start the webserver. Visual Studio Code allows you to debug Python very easily too.


### Run MySql database
Open a terminal and establish an SSH tunnel to the VM where the database is hosted

Run ssh -L localhost:54306:localhost:54306 username@cs506-team-01.cs.wisc.edu

--> enter cs password

Manage the database with any DBMS of preference

DATABASE_NAME = "othello"

DATABASE_USER = "root"

DATABASE_PASSWORD = "pass123"

DATABASE_HOST = "127.0.0.1"

DATABASE_PORT = "54306"

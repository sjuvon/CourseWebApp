# CourseWebApp README

Welcome!  This project is something I've wanted to do for a long time: make a proper web app for the courses I teach.  It's great to finally get the ball rolling.

The app is implemented in Flask together with the extensions Flask-WTF and Flask-CKEditor; for the back-end we have SQLite3 (for now) via SQLAlchemy.  The app's content itself is based on a course I taught in Spring 2019.

Everything's [up and running here on Heroku](https://coursewebapp.herokuapp.com/) (best viewed on Desktop).  For kicks, you can compare everything to the original static page I used in Spring '19—see: '7142.html'.  Check it all out!

Some helpful bits if you decide to clone the repository:

  1) The admin account is configured as follows:
  
        Username: *admin*  
        Password: *password*
  
  2) Once you have your [virtual environment set up](https://flask.palletsprojects.com/en/2.0.x/installation/) (Python, Flask, Flask-WTF, Flask-CKEditor, SQLAlchemy), fire up the app from its top directory with the usual Flask commands:
  
          $ export FLASK_APP=run.py
          $ export FLASK_ENV=development
          $ flask run
          
There's more to come—stay tuned for updates and more projects!

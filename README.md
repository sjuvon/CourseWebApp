# CourseWebApp README

Welcome to my first project in Flask!  I've taken this opportunity to do something I've wanted for a long time: make a proper web app for the courses I teach.  The present app is a first step towards that.

The app is implemented in Flask, using the extensions Flask-WTF and Flask-CKEditor; for the back-end we have SQLite3.  The app's content itself is based on a course I taught in Spring 2019.  Check it out!  For kicks, you can compare everything to the actual HTML page I used then—see: '7142.html'.

Some relevant info:

  1) The admin account is configured as follows:
  
        Username: *admin*  
        Password: *password*
  
  2) Once you have your virtual environment set up, fire up the app with the usual Flask commands:
  
          $ export FLASK_APP=run
          $ export FLASK_ENV=development
          $ flask run
          
  3) A SQLite database has been included for use—see: 'db.sqlite'.  You can initialise a new database instead with the following command (just before running Flask):
  
          $ flask db-init
          
      **However, you should skip this step and use the database as provided if you'd like to see the app as originally intended, based on that course from Spring 2019.**
  
Stay tuned for updates and more projects!

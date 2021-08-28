# CourseWebApp README

Welcome to my first project in Flask!  I've taken this opportunity to do something I've wanted for a long time: make a proper web app for the courses I teach.

This project has been a fun first step towards that.  The app is implemented in the Python framework Flask along with its extensions Flask-WTF and Flask-CKEditor; it currently uses SQLite3 for the back-end.  The app's content itself is based on a course I taught in Spring 2019—check it out!  You can also compare it to the actual HTML page I used back in '19—see: '7142.html'.

Some more comments:

  1) The admin account is configured as follows:
  
        Username: *admin*  
        Password: *password*
        
        The app has been written for now so that 'admin' is always the administrative account.
  
  2) Once you have your virtual environment set up, fire up the app with the usual Flask commands:
  
          $ export FLASK_APP=run
          $ export FLASK_ENV=development
          $ flask run
          
  3) A SQLite database has been included for use—see: 'db.sqlite'.  You can initialise a new database instead with the following command (just before running Flask):
  
          $ flask db-init
          
      **However, you should skip this step and use the database as provided if you'd like to see the app as originally intended, based on that course from Spring 2019.**
  
There's more to do from here.  Stay tuned for updates and more fun projects!

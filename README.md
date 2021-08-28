# CourseWebApp README!

Welcome!  After 10+ years of teaching at college, I've finally made a course website that I would've happily deployed for my students.  It comes in the form of a web app written in Python's Flask.  The app that's provided is based on a course I taught in Spring 2019.  Feel free to check it out!

Some comments:

  0) The admin account is configured as follows:
  
        Username: *admin*  
        Password: *password*
        
        The app has been written so that 'admin' is always the administrative account.  (See: 5) below for more on this.)

  1) The app uses the Python framework Flask with extensions Flask-WTF, Flask-CKEditor; it's also set up for SQLite3 as the back-end.  There's some JavaScript, so don't forget to allow scripts on your browser.
  
  2) Once you have those up and running in your virtual environment, fire up the app with the usual Flask commands:
  
          $ export FLASK_APP=run
          $ export FLASK_ENV=development
          $ flask run
          
  3) A SQLite database has been included for use—see: 'db.sqlite'.  You're welcome to initialise your own database instead with the following command (just before running Flask):
  
          $ flask db-init
          
      **However, I'd suggest using the db.sqlite provided if you'd like to see the site as originally intended, as it would have looked had I made the app in Spring '19.**
      
  4) Speaking of Spring '19, I've included a copy of the original course webpage from that semester ('7142.html').  See for yourself: it's great to finally have a proper app!
  
  5) Where do we go from here?  This has been a fun project in Flask, and I'd like to keep the fun going in two immediate directions:  
    - Go deeper with Flask by writing an extension for the app that manages Users, Roles and Permissions.  
    - Move laterally and work on a single-page version of the app in JavaScript.  

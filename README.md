# CourseWebApp README!

Welcome!  After 10+ years of teaching, I've finally made a course website that I would've happily deployed for my students.  Instead of being a basic HTML file, the site comes as a web app written in Python's Flask.  It's based on a course I taught in Spring 2019.  Check it out!

Some comments:

  0) The admin account is configured as follows:
  
        Username: *admin*  
        Password: *password*
        
        The app has been written for now so that 'admin' is always the administrative account.

  1) The app uses the Python framework Flask with extensions Flask-WTF, Flask-CKEditor; it also uses SQLite3 for the back-end.  There's some JavaScript, so don't forget to allow scripts on your browser.
  
  2) Once you have all of that set up in your virtual environment, fire up the app with the usual Flask commands:
  
          $ export FLASK_APP=run
          $ export FLASK_ENV=development
          $ flask run
          
  3) A SQLite database has been included for use—see: 'db.sqlite'.  You're welcome to initialise a new database instead with the following command (just before running Flask):
  
          $ flask db-init
          
      **However, you should skip this step if you'd like to see the site as originally intended, as it would have looked had the app been available in Spring '19.**
      
  4) Speaking of Spring '19, I've included a copy of the original course webpage from that semester ('7142.html').  See for yourself: it's great to finally have a proper app!
  
  5) Where do we go from here?  This has been a fun project in Flask, and I'd like to keep the fun going in several directions.  Stay tuned for updates and more exciting projects!

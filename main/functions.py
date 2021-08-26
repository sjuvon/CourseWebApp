### CourseWebApp.functions

import functools
import os

from flask import g
from flask import redirect
from flask import url_for
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from main.auth import views


### Login requirement decorator
def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			return redirect(url_for('auth.login'))
		return view(**kwargs)
	return wrapped_view
	

### Admin requirement decorator
def admin_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None or g.user['username'] != 'admin':			
			abort(403)
		return view(**kwargs)
	return wrapped_view


### For uploads
### 1) Preps files to be uploaded, and
### 2) Saves them to appropriate location.
### N.B. 2) currently has files saved to local disk.
###		 That would change if the app ever went into production.
def upload(file,location):
	if file is None:
		return
		
	filename = secure_filename(file.filename)
	destination = os.path.join(os.path.abspath(os.curdir),f"uploads/{location}")

	try:
		file.save(os.path.join(destination,filename))
	except:
		os.makedirs(destination)
		file.save(os.path.join(destination,filename))

	return filename


### Don't mind me, just doing my job
def debug(dictionary):
	with open( 'file.py', 'a+' ) as F:
		F.write( "\n" + repr(dictionary) + "\n" )


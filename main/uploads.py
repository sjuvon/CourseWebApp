### CourseWebApp.uploads
"""
	Module for uploads function
								"""

import functools
import os

from flask import g
from flask import redirect
from flask import url_for
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from main.auth import views


### For uploads.  This:
### 1) Preps files to be uploaded, and
### 2) Saves them to appropriate location.
### N.B. 2) currently has files saved to local disk.
###		That would change to the server
###		if the app ever went into production.
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


### Don't mind me, just doin' my job
def debug(dictionary):
	with open( 'file.py', 'a+' ) as F:
		F.write( "\n" + repr(dictionary) + "\n" )


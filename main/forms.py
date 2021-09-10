"""
    Module for creating webforms used throughout app.

    E.g., See modules:
            'main.announcements'
            'main.homework'
            'main.lectures'
            'main.welcome'  (Located in 'main.view')
    N.B. The Authentication module 'main.auth'
    uses its own special forms.
"""
from flask import flash, g
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError

from main.homework.models import Homework
from main.lectures.models import Lecture


def formula_create(*args, **kwargs):
    """ Factory for creating posts """
    class Form_Create(FlaskForm):
        submit = SubmitField()

        def outtakes(self):
            """ For displaying validation errors in user input """
            if self.errors:
                for error in self.errors.values():
                    flash(*error)

        def validate_Zahl(self,Zahl):
            """ To verify that we're creating a valid lecture/assignment """
            if self.table == 'homework':
                check_exists = Homework.query.filter_by(id=self.Zahl.data).first()
                if check_exists:
                    raise ValidationError(f"Homework {self.Zahl.data} already exists")
            elif self.table == 'lecture':
                check_exists = Lecture.query.filter_by(id=self.Zahl.data).first()
                if check_exists:
                    raise ValidationError(f"Lecture {self.Zahl.data} already exists")


    ### The portion of the factory that makes a form's fields.
    ### This depends on user input, which we organise into
    ### two parts:
    ###     (1) Database-specifics
    ###     (2) FlaskForm fields
    ### Note: The kwarg-values are strings.

    Fach = { 'File', 'Integer', 'String', 'TextArea', 'CKEditor' }
    for key, value in kwargs.items():
        if value not in Fach:
            if key == 'table':
                setattr( Form_Create, key, value )
            else:
                raise ValidationError("Oops!  Incorrect keyword argument(s).")
        else:   
            label = f"{key}".capitalize()
            field = eval(f"{value}Field")(label)
            setattr( Form_Create, f"{key}", field )


    return Form_Create()
                                                                    ### END CLASS Form_Create


def formula_update(**kwargs):
    """
    Factory for updating posts

    Virtually everything below is the same as above.  The
    only differences are:
        (1) The dictionary attribute formContent,
        (2) kwarg-values here may be tuples in addition to strings.
    """
    class Form_Update(FlaskForm):
        submit = SubmitField()
        formContent = {}

        def outtakes(self):
            if self.errors:
                for error in self.errors.values():
                    flash(*error)       

        def validate_Zahl(self,Zahl):
            """ To verify that we're updating the correct lecture/assignment """
            if self.table == 'homework':
                check_exists = Homework.query.filter_by(id=self.Zahl.data).first()
                
                if self.Zahl.data != self.id:
                    raise ValidationError(f"Homework {self.Zahl.data} already exists.  This is Homework {self.id}.") if check_exists \
                        else ValidationError(f"Homework {self.Zahl.data} does not exist.  This is Homework {self.id}.")

            elif self.table == 'lecture':
                check_exists = Lecture.query.filter_by(id=self.Zahl.data).first()

                if self.Zahl.data != self.id:
                    raise ValidationError(f"Lecture {self.Zahl.data} already exists.  This is Lecture {self.id}.") if check_exists \
                        else ValidationError(f"Lecture {self.Zahl.data} does not exist.  This is Lecture {self.id}.")


    ### Again, the values here can be tuples:
    Fach = { 'File', 'Integer', 'String', 'TextArea', 'CKEditor' }
    for key, value in kwargs.items():
        if type(value) != tuple:
            if key == 'table' or key == 'id':
                setattr( Form_Update, key, value)
                Form_Update.formContent[key] = value
            else:
                raise ValidationError(f"Oops! Incorrect keyword argument(s).")
        elif value[0] not in Fach:
            raise ValidationError(f"Oops!  Incorrect keyword argument(s).")
        else:
            label = f"{key}".capitalize()
            field = eval(f"{value[0]}Field")(label)
            setattr( Form_Update, f"{key}", field )

            Form_Update.formContent[key] = value[1]


    return Form_Update(**Form_Update.formContent)
                                                                    ### END CLASS Form_Update



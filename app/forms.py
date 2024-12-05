from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

class UploadForm(FlaskForm):
    document = FileField('Upload Document', 
                        validators=[
                            FileRequired(),
                            FileAllowed(['docx', 'txt'], 'Please upload a Word or text document')
                        ])
    submit = SubmitField('Process Document')

from flask import Blueprint, render_template, request, send_file, flash, redirect, url_for, current_app, make_response
from werkzeug.utils import secure_filename
import os
from app.processor.document import DocumentProcessor
from app.forms import UploadForm

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    if request.method == 'POST' and form.validate_on_submit():
        file = form.document.data
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                processor = DocumentProcessor(filepath)
                processed_text = processor.process()
                
                # Clean up original file
                os.remove(filepath)
                
                # Create response with processed text
                response = make_response(processed_text)
                response.headers['Content-Type'] = 'text/plain'
                response.headers['Content-Disposition'] = f'attachment; filename=processed_{filename}'
                
                return response
                
            except Exception as e:
                flash(f'Error processing file: {str(e)}', 'error')
                return redirect(url_for('main.index'))
    
    return render_template('index.html', form=form)
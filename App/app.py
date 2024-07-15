from flask import Flask, request, render_template, redirect, url_for, abort
from werkzeug.utils import secure_filename
import os
from helpers import allowed_file
from pdf_processor import extract_text_from_pdf
from docx_processor import extract_text_from_docx
from csv_processor import extract_text_from_csv
from txt_processor import extract_text_from_txt
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object('config')

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('html/index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return 'No file part'
        
        file = request.files['file']
        
        if file.filename == '':
            return 'No selected file'
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            return redirect(url_for('view_file', filename=filename))
        
        else:
            return 'Formato de archivo no válido'
    
    except Exception as e:
        return f'Error al subir el archivo: {str(e)}'

@app.route('/view_file/<filename>')
def view_file(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if filename.lower().endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif filename.lower().endswith(('.doc', '.docx')):
            text = extract_text_from_docx(file_path)
        elif filename.lower().endswith('.csv'):
            text = extract_text_from_csv(file_path)
        elif filename.lower().endswith('.txt'):
            text = extract_text_from_txt(file_path)
        else:
            abort(400, 'Tipo de archivo no soportado')
        
        return render_template('html/view_file.html', filename=filename, text=text)
    
    except Exception as e:
        return f'Error al procesar el archivo: {str(e)}'

# Agregar rutas para las demás páginas
@app.route('/index')
def volver():
    return render_template('html/index.html')

@app.route('/contacto')
def contacto():
    return render_template('html/contacto.html')

@app.route('/faqs')
def faqs():
    return render_template('html/faqs.html')

@app.route('/iniciar-sesion')
def iniciar_sesion():
    return render_template('html/iniciar-sesion.html')

@app.route('/recursos')
def recursos():
    return render_template('html/recursos.html')

@app.route('/upload')
def upload():
    return render_template('html/upload.html')

@app.route('/quienes-somos')
def quienes_somos():
    return render_template('html/quienes-somos.html')

if __name__ == '__main__':
    app.run(debug=True)

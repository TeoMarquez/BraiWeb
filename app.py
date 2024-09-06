from flask import Flask, render_template, request, redirect, url_for, flash, abort, jsonify, make_response, send_file
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
import weasyprint
import os
from helpers import allowed_file
from pdf_processor import extract_text_from_pdf
from docx_processor import extract_text_from_docx
from csv_processor import extract_text_from_csv
from txt_processor import extract_text_from_txt
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from models import db, User
from queries import register_user
import stripe

from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object('config')

# Configuracion de Pasarella
stripe.api_key = app.config['STRIPE_TEST_SECRET_KEY']


# Configuración de SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345678@localhost/braiNet'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Inicializa SQLAlchemy

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
    
@app.route('/download_file/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Procesa el archivo dependiendo de su formato
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
        
        # Renderiza la plantilla HTML solo con el contenido para el PDF
        rendered_html = render_template('html/pdf_content.html', filename=filename, text=text)
                
        # Generar PDF con WeasyPrint
        pdf = weasyprint.HTML(string=rendered_html).write_pdf()
        
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename={filename}.pdf'
        
        return response
    
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        success, error = register_user(name, email, password, confirm_password)
        if success:
            print('Registro exitoso. Puedes iniciar sesión ahora.')
            return redirect(url_for('signin'))
        else:
            print(f'Error al registrar la cuenta: {error}')
            return render_template('html/register.html', error=error)

    return render_template('html/register.html')

@app.route('/recursos')
def recursos():
    return render_template('html/recursos.html')

@app.route('/upload')
def upload():
    return render_template('html/upload.html')

@app.route('/about')
def about():
    return render_template('html/about.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        success, error, user_id, is_premium = check_user_credentials(email, password)
        if success:
            print('Inicio de sesión exitoso.')
            return jsonify({
                'success': True,
                'user_id': user_id,
                'is_premium': is_premium
            })
        else:
            print(f'Error al iniciar sesión: {error}')
            return jsonify({
                'success': False,
                'error': error
            })

    return render_template('html/signin.html')

def check_user_credentials(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        return True, None, user.id, user.is_premium
    else:
        return False, "Correo electrónico o contraseña incorrectos.", None, None


@app.route('/myprofile')
def myprofile():
    return render_template('html/view-user.html')

@app.route('/profilePremium')
def profilePremium():
    return render_template('html/view-user-premium.html')

@app.route('/get_user_info', methods=['GET'])
def get_user_info():
    user_id = request.args.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            return jsonify({
                'name': user.name,
                'email': user.email,
                'plan': 'Premium' if user.is_premium else 'No Premium'
            })
        return jsonify({'error': 'Usuario no encontrado'}), 404
    return jsonify({'error': 'No se proporcionó ID de usuario'}), 400


@app.route('/update_to_premium', methods=['POST'])
def update_to_premium():
    data = request.get_json()
    user_id = data['user_id']

    user = User.query.get(user_id)
    if user:
        user.is_premium = True
        try:
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    

@app.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    data = request.get_json()
    try:
        intent = stripe.PaymentIntent.create(
            amount=data['amount'],  # En centavos
            currency='Ars',         # Cambia la moneda según tus necesidades
            payment_method_types=['card']
        )
        return jsonify({'client_secret': intent.client_secret})
    except stripe.error.StripeError as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

import os
import pandas as pd
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from app import app, db
from app.models import Disease, Supplement
from models.model_utils import load_model, predict_disease

# Create uploads directory if it doesn't exist
os.makedirs('static/uploads', exist_ok=True)

# Load the model
MODEL_PATH = os.path.join(app.root_path, '../models/plant_disease_model_1.pt')
try:
    model = load_model(MODEL_PATH)
except Exception as e:
    print(f"Error loading model: {str(e)}")
    model = None

# Load data from CSV files if database is empty
def initialize_data():
    if Disease.query.count() == 0:
        try:
            # Load disease information
            disease_df = pd.read_csv(os.path.join(app.root_path, '../data/disease_info.csv'), encoding='cp1252')
            supplement_df = pd.read_csv(os.path.join(app.root_path, '../data/supplement_info.csv'), encoding='cp1252')
            
            # Add diseases to the database
            for _, row in disease_df.iterrows():
                disease = Disease(
                    id=row['index'],
                    name=row['disease_name'],
                    description=row['description'],
                    possible_steps=row['Possible Steps'],
                    image_url=row['image_url']
                )
                db.session.add(disease)
            
            # Add supplements to the database
            for _, row in supplement_df.iterrows():
                # Skip empty rows
                if pd.isna(row['supplement name']):
                    continue
                    
                supplement = Supplement(
                    disease_id=row['index'],
                    name=row['supplement name'],
                    image_url=row['supplement image'],
                    buy_link=row['buy link']
                )
                db.session.add(supplement)
            
            db.session.commit()
            print("Database initialized with disease and supplement data")
        except Exception as e:
            db.session.rollback()
            print(f"Error initializing database: {str(e)}")

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Disease prediction page
@app.route('/predict', methods=['GET'])
def predict_page():
    return render_template('predict.html')

# API endpoint for image upload and prediction
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['image']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    # Secure the filename to prevent any security issues
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.root_path, '../static/uploads', filename)
    
    # Save the file
    file.save(file_path)
    
    # Perform prediction
    try:
        if model is None:
            raise RuntimeError("Model not loaded")
        
        prediction_idx, _ = predict_disease(model, file_path)
        
        # Redirect to results page
        return redirect(url_for('prediction_result', prediction_id=prediction_idx, image=filename))
    except Exception as e:
        return render_template('error.html', error=str(e))

# Results page
@app.route('/result/<int:prediction_id>/<image>')
def prediction_result(prediction_id, image):
    # Get disease information from database
    disease = Disease.query.get_or_404(prediction_id)
    
    # Get supplement information for this disease
    supplement = Supplement.query.filter_by(disease_id=prediction_id).first()
    
    return render_template('result.html', 
                           disease=disease,
                           supplement=supplement,
                           image_file=image)

# Supplements page
@app.route('/supplements')
def supplements_page():
    supplements = Supplement.query.all()
    diseases = Disease.query.all()
    
    return render_template('supplements.html', 
                           supplements=supplements,
                           diseases=diseases)

# About page
@app.route('/about')
def about_page():
    return render_template('about.html')

# Contact page
@app.route('/contact')
def contact_page():
    return render_template('contact.html')

# Serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(app.root_path, '../static/uploads'), filename)

# Initialize the database
with app.app_context():
    db.create_all()
    initialize_data() 
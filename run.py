import os
import shutil
import pandas as pd
from app import app

# Create required directories
os.makedirs('static/uploads', exist_ok=True)
os.makedirs('data', exist_ok=True)
os.makedirs('models', exist_ok=True)

# Check for model file
model_path = 'models/plant_disease_model_1.pt'
if not os.path.exists(model_path):
    print("WARNING: Model file not found!")
    print("Please ensure the model file is present in the models directory")
    print("You can download it using: python download_model.py")

# Check for data files
data_files = [
    ('disease_info.csv', 'data/disease_info.csv'),
    ('supplement_info.csv', 'data/supplement_info.csv')
]

for data_file, dst_path in data_files:
    if not os.path.exists(dst_path):
        print(f"WARNING: Data file {data_file} not found!")
        print(f"Please ensure {data_file} is present in the data directory")

# Print startup information
print("")
print("=" * 50)
print("Plant Disease Detection Application")
print("=" * 50)
print(f"Model loaded: {'Yes' if os.path.exists(model_path) else 'No'}")
print(f"Data files available: {all(os.path.exists(f'data/{file}') for file, _ in data_files)}")
print("=" * 50)
print("")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') 
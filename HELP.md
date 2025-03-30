# Plant Disease Detection Application - Help Guide

## Getting Started

### Prerequisites
- Python 3.8 or newer
- pip package manager

### Setup Instructions

1. **Set up a virtual environment:**
   ```
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```
   python run.py
   ```

5. **Access the application:**
   Open your web browser and navigate to http://localhost:5000

## Troubleshooting

### Installation Issues

If you encounter issues with dependencies, try the following:

1. **Install packages with binary wheels:**
   ```
   pip install --only-binary :all: pillow pandas torch torchvision
   ```

2. **For torch/torchvision issues:**
   Visit the official PyTorch website and use their installation selector
   to get the appropriate command for your system:
   https://pytorch.org/get-started/locally/

3. **For Microsoft Visual C++ errors:**
   Download and install Microsoft Visual C++ Build Tools from:
   https://visualstudio.microsoft.com/visual-cpp-build-tools/

### Application Issues

1. **Model loading errors:**
   - Ensure the model file (`plant_disease_model_1.pt`) is in the `models/` directory
   - Check that the correct version of PyTorch is installed

2. **Image upload issues:**
   - Make sure the `static/uploads` directory exists and is writable
   - Check that Pillow is installed correctly

3. **Database errors:**
   - Verify that the CSV data files are in the `data/` directory
   - Check the Flask-SQLAlchemy configuration in `app/__init__.py`

## Contact Support

For additional help, please contact:
- Email: support@plantdiseasedetection.com
- GitHub: https://github.com/yourusername/plant-disease-detection

## License
This project is licensed under the MIT License - see the LICENSE file for details. 
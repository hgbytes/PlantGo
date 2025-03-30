import gdown

# Replace this with your actual Google Drive file ID
file_id = "1d54wF23ZQpK0LlBkA0_ZloDDcgt0GPP9"
url = f"https://drive.google.com/uc?id={file_id}"
output = "models/plant_disease_model_1.pt"

gdown.download(url, output, quiet=False)

# Plant Disease Detection API 🌿

This API provides plant disease detection capabilities using a deep learning model. Upload an image of a plant leaf, and the API will identify potential diseases and provide treatment recommendations.

## API Endpoints

### Health Check
```http
GET /health
```
Returns the status of the API and model.

### Predict Disease
```http
POST /predict
```
Upload an image file to get disease prediction and treatment recommendations.

## Example Usage

```python
import requests

# Replace with your Space URL
API_URL = "https://hgbytes-plantgoai.hf.space"

# Health check
response = requests.get(f"{API_URL}/health")
print(response.json())

# Make prediction
with open("plant_image.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post(f"{API_URL}/predict", files=files)
    print(response.json())
```

## Response Format

```json
{
    "disease_name": "Disease Name",
    "disease_info": {
        "description": "Disease description",
        "possible_steps": "Treatment steps",
        "image_url": "Reference image URL"
    },
    "supplements": [
        {
            "supplement_name": "Recommended supplement",
            "image_url": "Product image",
            "buy_link": "Purchase link"
        }
    ]
}
```

## Supported Plants
- Apple 🍎
- Blueberry 🫐
- Cherry 🍒
- Corn 🌽
- Grape 🍇
- Orange 🍊
- Peach 🍑
- Pepper 🫑
- Potato 🥔
- Raspberry
- Soybean
- Squash
- Strawberry 🍓
- Tomato 🍅

## Model Information
- Architecture: CNN (Convolutional Neural Network)
- Input: RGB images (224x224 pixels)
- Output: 39 disease classes
- Accuracy: High accuracy on common plant diseases

## License
MIT License 
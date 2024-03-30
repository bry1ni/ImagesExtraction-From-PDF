import torch
import clip
import numpy as np
from transformers import CLIPProcessor, CLIPModel


# Load the CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)


# Function to generate embeddings for images and text
def generate_embeddings(images, texts):
    image_features = []
    text_features = []
    for image, text in zip(images, texts):
        inputs = processor(text=text, images=image, return_tensors="pt", padding=True, truncation=True).to(device)
        with torch.no_grad():
            outputs = model(**inputs)

        image_embedding = outputs.last_hidden_state[:, 0, :]
        text_embedding = outputs.pooler_output
        image_features.append(image_embedding.cpu().numpy())
        text_features.append(text_embedding.cpu().numpy())

    return np.array(image_features), np.array(text_features)


import clip
import torch
from PIL import Image

model, preprocess = clip.load("ViT-B/32", device="cpu")
image = preprocess(Image.open("./sample_img/cat.png")).unsqueeze(0)
texts = clip.tokenize(["a dog", "a cat", "a car"])

with torch.no_grad():
    image_features = model.encode_image(image)
    text_features = model.encode_text(texts)

# Compare which text matches the image
logits_per_image, logits_per_text = model(image, texts)
probs = logits_per_image.softmax(dim=-1).cpu().detach().numpy() 
print("Label probs:", probs)
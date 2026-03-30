from pathlib import Path
from PIL import Image, UnidentifiedImageError
import torch
import clip

# Define supported types
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"}

def load_images_from_folder(folder_path: str, preprocess, device):
    folder = Path(folder_path)
    
    image_tensors = []
    valid_paths = []

    for file_path in sorted(folder.iterdir()):
        # Skip unsupported file types
        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            print(f"Skipping {file_path.name} — unsupported type")
            continue
        
        try:
            img = Image.open(file_path).convert("RGB")  # normalize to RGB
            tensor = preprocess(img).unsqueeze(0).to(device)
            image_tensors.append(tensor)
            valid_paths.append(file_path)
            
        except UnidentifiedImageError:
            print(f"Skipping {file_path.name} — not a valid image")
        except Exception as e:
            print(f"Skipping {file_path.name} — {e}")

    if not image_tensors:
        raise ValueError(f"No valid images found in {folder_path}")

    return torch.cat(image_tensors, dim=0), valid_paths


# Usage
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

images, paths = load_images_from_folder("sample_img", preprocess, device)
text = clip.tokenize(["a photo of a cat"]).to(device)

with torch.no_grad():
    image_features = model.encode_image(images)
    text_features = model.encode_text(text)

similarities = (image_features @ text_features.T).squeeze()
best_match_idx = similarities.argmax().item()

# Now gives you the actual filename, not just an index
print(f"Best matching image: {paths[best_match_idx].name}")
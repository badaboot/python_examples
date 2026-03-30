import sys
import torch
import clip
from pathlib import Path
from PIL import Image, UnidentifiedImageError

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"}

def load_images_from_folder(folder_path: str, preprocess, device):
    folder = Path(folder_path)
    
    image_tensors = []
    valid_paths = []

    for file_path in sorted(folder.iterdir()):
        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            print(f"Skipping {file_path.name} — unsupported type")
            continue
        
        try:
            img = Image.open(file_path).convert("RGB")
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


def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <folder_path> <query>")
        print('Example: python script.py ./images "elaborate chinese court costume"')
        sys.exit(1)

    folder_path = sys.argv[1]
    query = " ".join(sys.argv[2:])  # joins remaining args, so quotes are optional

    print(f"Folder: {folder_path}")
    print(f"Query:  {query}")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)

    images, paths = load_images_from_folder(folder_path, preprocess, device)
    text = clip.tokenize([query]).to(device)

    with torch.no_grad():
        image_features = model.encode_image(images)
        text_features = model.encode_text(text)

    similarities = (image_features @ text_features.T).squeeze()
    best_match_idx = similarities.argmax().item()

    print(f"\nBest match: {paths[best_match_idx].name}")
    print(f"Similarity score: {similarities[best_match_idx]:.4f}")

    # Optional: show top 5
    top_k = min(5, len(paths))
    top_indices = similarities.topk(top_k).indices
    print(f"\nTop {top_k} matches:")
    for rank, idx in enumerate(top_indices, 1):
        print(f"  {rank}. {paths[idx].name} ({similarities[idx]:.4f})")


if __name__ == "__main__":
    main()
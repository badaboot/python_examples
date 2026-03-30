import torch
import clip
from pathlib import Path
from PIL import Image, UnidentifiedImageError
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"}

# Load model once at startup
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

app.mount("/static", StaticFiles(directory="./static"), name="static")
IMAGES_FOLDER = "../sample_img"
@app.get("/")
def serve_index():
    return FileResponse("index.html")

# Mount after app is created — use the same IMAGES_FOLDER variable
app.mount("/images", StaticFiles(directory=IMAGES_FOLDER), name="images")

def load_images_from_folder():
    folder = Path(IMAGES_FOLDER)
    image_tensors = []
    valid_paths = []

    for file_path in sorted(folder.iterdir()):
        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
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
        raise ValueError(f"No valid images found in {IMAGES_FOLDER}")

    return torch.cat(image_tensors, dim=0), valid_paths


def search_images(query: str, top_k: int = 5):
    images, paths = load_images_from_folder()
    text = clip.tokenize([query]).to(device)

    with torch.no_grad():
        image_features = model.encode_image(images)
        text_features = model.encode_text(text)

    similarities = (image_features @ text_features.T).squeeze()

    # Handle single image edge case
    if similarities.dim() == 0:
        similarities = similarities.unsqueeze(0)

    top_k = min(top_k, len(paths))
    top_indices = similarities.topk(top_k).indices

    results = []
    for rank, idx in enumerate(top_indices, 1):
        results.append({
            "rank": rank,
            "filename": paths[idx].name,
            "filepath": str(paths[idx]),
            "score": round(similarities[idx].item(), 4)
        })

    return results


@app.post("/search")
def search(req: QueryRequest):
    try:
        results = search_images(req.query, req.top_k)
        return {"query": IMAGES_FOLDER, "results": results}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    return {"status": "ok", "device": device}


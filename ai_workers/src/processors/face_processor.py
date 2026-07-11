from src.processors.image_processor import load_image
import cv2
from src.config import DATA_DIR, FACES_OUTPUT_DIR
from pathlib import Path
import cv2

sample_image = DATA_DIR / "sample_images" / "group_img.jpg"
CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def detect_faces(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return CASCADE.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
    )

def crop_faces(image, boxes):
    faces = []

    for (x, y, w, h) in boxes:
        face = image[y:y+h, x:x+w]
        if face.size > 0:
            faces.append(face)

    return faces

def save_faces(faces, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)

    saved_paths = []

    for i, face in enumerate(faces):
        path = output_dir / f"face_{i:04d}.jpg"
        cv2.imwrite(str(path), face)
        saved_paths.append(path)

    return saved_paths

def process_faces(image_path: Path):
    image = load_image(image_path)
    boxes = detect_faces(image)
    faces = crop_faces(image, boxes)
    saved_paths = save_faces(faces, FACES_OUTPUT_DIR)

    return {
        "face_count": len(faces),
        "bounding_boxes": [tuple(map(int, b)) for b in boxes],
        "saved_faces": saved_paths,
    }


if __name__ == "__main__":
    result = process_faces(sample_image)
    print(f"Detected {result['face_count']} face(s)")
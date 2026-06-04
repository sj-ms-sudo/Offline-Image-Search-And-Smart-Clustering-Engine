from utils.path_utils import get_image_files
from utils.image_utils import load_image
from detector.detector import create_detector
from detector.detector import detect_faces
from utils.image_utils import draw_rectangle
from utils.path_utils import create_output_path
from utils.image_utils import save_image
def main():
    detector = create_detector()
    path = "../photos"
    images = get_image_files(path)
    image_count = len(images)
    for index ,image_path in enumerate(images,start=1):
        print(f"[{index}/{image_count}] Processing {image_path.name}")
        image = load_image(image_path)

        faces = detect_faces(image,detector)

        image = draw_rectangle(image,faces)

        output_path = create_output_path(image_path)

        save_image(image,output_path)

        print(f"Saved {output_path}\n")

if __name__ == "__main__":
    main()
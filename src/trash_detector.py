# trash_detector.py

from ultralytics import YOLO
from categories import CATEGORIES

def load_and_tune_model(model_path="yolov8s-worldv2.pt", save_path="prompt_tuned_trash.pt"):
    """
    Load YOLO-World model and apply prompt tuning for trash classification.
    """
    model = YOLO(model_path)

    # Flatten all subcategories into prompts
    prompts = []
    class_mapping = {}
    for main_class, sub_classes in CATEGORIES.items():
        for sub in sub_classes:
            prompts.append(sub)
            class_mapping[sub] = main_class

    model.set_classes(prompts)
    model.save(save_path)

    print(f"✅ Model tuned and saved to {save_path}")
    return save_path, class_mapping


if __name__ == "__main__":
    load_and_tune_model()


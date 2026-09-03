"""
YOLOv8n Training from Scratch

Smart Campus Surveillance System

This module trains the YOLOv8n architecture from scratch
using the project's custom Person detection dataset.

Pretrained YOLO weights are NOT used.
"""

from pathlib import Path

from ultralytics import YOLO


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_YAML = PROJECT_ROOT / "data" / "dataset" / "data.yaml"

OUTPUT_DIR = PROJECT_ROOT / "runs"


# ---------------------------------------------------------
# Training configuration
# ---------------------------------------------------------

MODEL_CONFIG = "yolov8n.yaml"

IMAGE_SIZE = 640
EPOCHS = 50
BATCH_SIZE = 4
WORKERS = 0

PROJECT_NAME = "smart_campus_yolov8n"


def validate_dataset():
    """Verify that the dataset configuration exists."""

    if not DATASET_YAML.exists():
        raise FileNotFoundError(
            f"Dataset configuration not found: {DATASET_YAML}"
        )

    print(f"Dataset configuration: {DATASET_YAML}")
    print("Dataset configuration found.")


def create_model():
    """
    Create YOLOv8n architecture without pretrained weights.

    Using the YAML architecture file ensures that pretrained
    .pt weights are not loaded.
    """

    print("\nCreating YOLOv8n architecture...")
    print("Pretrained weights: DISABLED")

    model = YOLO(MODEL_CONFIG)

    print("YOLOv8n architecture created successfully.")

    return model


def train_model(model):
    """Train YOLOv8n from scratch."""

    print("\nStarting training...")
    print("----------------------------------------")
    print(f"Dataset : {DATASET_YAML}")
    print(f"Model   : {MODEL_CONFIG}")
    print(f"Epochs  : {EPOCHS}")
    print(f"Batch   : {BATCH_SIZE}")
    print(f"Image   : {IMAGE_SIZE}")
    print("Device  : CPU")
    print("----------------------------------------\n")

    results = model.train(
        data=str(DATASET_YAML),
        epochs=EPOCHS,
        imgsz=IMAGE_SIZE,
        batch=BATCH_SIZE,
        workers=WORKERS,
        device="cpu",
        project=str(OUTPUT_DIR),
        name=PROJECT_NAME,
        pretrained=False,
        exist_ok=True,
        verbose=True,
    )

    return results


def main():
    """Main training entry point."""

    try:
        print("=" * 60)
        print("SMART CAMPUS SURVEILLANCE")
        print("YOLOv8n TRAINING FROM SCRATCH")
        print("=" * 60)

        validate_dataset()

        model = create_model()

        train_model(model)

        print("\n" + "=" * 60)
        print("TRAINING COMPLETED")
        print("=" * 60)

        best_model = (
            OUTPUT_DIR
            / "detect"
            / PROJECT_NAME
            / "weights"
            / "best.pt"
        )

        last_model = (
            OUTPUT_DIR
            / "detect"
            / PROJECT_NAME
            / "weights"
            / "last.pt"
        )

        print(f"\nBest model: {best_model}")
        print(f"Last model: {last_model}")

        if best_model.exists():
            print("\nSUCCESS: best.pt was created.")
        else:
            print("\nWARNING: best.pt was not found.")

    except Exception as error:
        print("\nTRAINING FAILED")
        print(f"Error: {error}")
        raise


if __name__ == "__main__":
    main()
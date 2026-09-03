"""
YOLOv8n Fine-Tuning

Smart Campus Surveillance System

This module fine-tunes a pretrained YOLOv8n model
on the project's custom Person detection dataset.

Unlike the custom-from-scratch experiment, this model
starts from official pretrained YOLOv8n weights.
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

PRETRAINED_MODEL = "yolov8n.pt"

IMAGE_SIZE = 640

# Final training duration for Model 2
EPOCHS = 10

BATCH_SIZE = 4
WORKERS = 0

PROJECT_NAME = "finetuned_yolov8n"


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
    Load the official pretrained YOLOv8n model.

    The pretrained weights provide the initial learned
    representation, which is then fine-tuned using the
    project's custom dataset.
    """

    print("\nLoading pretrained YOLOv8n...")
    print(f"Model: {PRETRAINED_MODEL}")
    print("Training type: Fine-tuning")

    model = YOLO(PRETRAINED_MODEL)

    print("Pretrained YOLOv8n loaded successfully.")

    return model


def train_model(model):
    """Fine-tune YOLOv8n on the custom dataset."""

    print("\nStarting fine-tuning...")
    print("----------------------------------------")
    print(f"Dataset     : {DATASET_YAML}")
    print(f"Model       : {PRETRAINED_MODEL}")
    print(f"Epochs      : {EPOCHS}")
    print(f"Batch       : {BATCH_SIZE}")
    print(f"Image       : {IMAGE_SIZE}")
    print("Device      : CPU")
    print("Pretrained  : True")
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
        pretrained=True,
        exist_ok=True,
        verbose=True,
    )

    return results


def main():
    """Main fine-tuning entry point."""

    try:
        print("=" * 60)
        print("SMART CAMPUS SURVEILLANCE")
        print("YOLOv8n FINE-TUNING")
        print("=" * 60)

        validate_dataset()

        model = create_model()

        train_model(model)

        print("\n" + "=" * 60)
        print("FINE-TUNING COMPLETED")
        print("=" * 60)

        # Ultralytics creates the output directly under
        # OUTPUT_DIR when project=OUTPUT_DIR is supplied.
        run_directory = OUTPUT_DIR / PROJECT_NAME

        best_model = run_directory / "weights" / "best.pt"
        last_model = run_directory / "weights" / "last.pt"

        print(f"\nRun directory: {run_directory}")
        print(f"Best model   : {best_model}")
        print(f"Last model   : {last_model}")

        if best_model.exists():
            print("\nSUCCESS: best.pt was created.")
        else:
            print("\nWARNING: best.pt was not found.")

        if last_model.exists():
            print("SUCCESS: last.pt was created.")
        else:
            print("WARNING: last.pt was not found.")

    except Exception as error:
        print("\nFINE-TUNING FAILED")
        print(f"Error: {error}")
        raise


if __name__ == "__main__":
    main()
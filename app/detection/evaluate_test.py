"""
YOLOv8n Test-Set Evaluation

Smart Campus Surveillance System

Evaluates the fine-tuned YOLOv8n model on the independent
test dataset and saves evaluation metrics and plots.
"""

from pathlib import Path

from ultralytics import YOLO


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_YAML = PROJECT_ROOT / "data" / "dataset" / "data.yaml"

MODEL_PATH = (
    PROJECT_ROOT
    / "runs"
    / "finetuned_yolov8n"
    / "weights"
    / "best.pt"
)

OUTPUT_DIR = PROJECT_ROOT / "runs" / "test_finetuned_yolov8n"


# ---------------------------------------------------------
# Evaluation configuration
# ---------------------------------------------------------

IMAGE_SIZE = 640
BATCH_SIZE = 4
WORKERS = 0


def validate_paths():
    """Verify that required files exist."""

    if not DATASET_YAML.exists():
        raise FileNotFoundError(
            f"Dataset configuration not found: {DATASET_YAML}"
        )

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model weights not found: {MODEL_PATH}"
        )

    print(f"Dataset: {DATASET_YAML}")
    print(f"Model  : {MODEL_PATH}")

    print("Required files verified.")


def load_model():
    """Load the trained fine-tuned YOLOv8n model."""

    print("\nLoading fine-tuned YOLOv8n model...")

    model = YOLO(str(MODEL_PATH))

    print("Model loaded successfully.")

    return model


def evaluate_model(model):
    """Evaluate the model on the independent test split."""

    print("\nStarting test-set evaluation...")
    print("----------------------------------------")
    print(f"Dataset : {DATASET_YAML}")
    print(f"Model   : {MODEL_PATH}")
    print("Split   : test")
    print(f"Image   : {IMAGE_SIZE}")
    print(f"Batch   : {BATCH_SIZE}")
    print("Device  : CPU")
    print("----------------------------------------\n")

    results = model.val(
        data=str(DATASET_YAML),
        split="test",
        imgsz=IMAGE_SIZE,
        batch=BATCH_SIZE,
        workers=WORKERS,
        device="cpu",
        project=str(OUTPUT_DIR.parent),
        name=OUTPUT_DIR.name,
        exist_ok=True,
        plots=True,
        verbose=True,
    )

    return results


def print_metrics(results):
    """Print important test-set metrics."""

    print("\n" + "=" * 60)
    print("TEST-SET RESULTS")
    print("=" * 60)

    try:
        print(
            f"Precision : {results.box.mp:.4f}"
        )
        print(
            f"Recall    : {results.box.mr:.4f}"
        )
        print(
            f"mAP50     : {results.box.map50:.4f}"
        )
        print(
            f"mAP50-95  : {results.box.map:.4f}"
        )
    except AttributeError:
        print("Metrics were generated but could not be read directly.")

    print("=" * 60)


def main():
    """Main evaluation entry point."""

    try:
        print("=" * 60)
        print("SMART CAMPUS SURVEILLANCE")
        print("FINE-TUNED YOLOV8N TEST EVALUATION")
        print("=" * 60)

        validate_paths()

        model = load_model()

        results = evaluate_model(model)

        print_metrics(results)

        print("\n" + "=" * 60)
        print("TEST EVALUATION COMPLETED")
        print("=" * 60)

        print(f"\nEvaluation output: {OUTPUT_DIR}")

    except Exception as error:
        print("\nTEST EVALUATION FAILED")
        print(f"Error: {error}")
        raise


if __name__ == "__main__":
    main()
"""
YOLOv8n Model Comparison

Smart Campus Surveillance System

Compares three YOLOv8n configurations using the
same test-set evaluation metrics:

1. Official pretrained YOLOv8n
2. YOLOv8n trained from scratch
3. Fine-tuned YOLOv8n

All models are evaluated on the same custom
Person detection test dataset.
"""

from pathlib import Path

from ultralytics import YOLO


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_YAML = PROJECT_ROOT / "data" / "dataset" / "data.yaml"

PRETRAINED_MODEL = PROJECT_ROOT / "yolov8n.pt"

SCRATCH_MODEL = (
    PROJECT_ROOT
    / "runs"
    / "detect"
    / "runs"
    / "baseline_scratch"
    / "weights"
    / "best.pt"
)

FINETUNED_MODEL = (
    PROJECT_ROOT
    / "runs"
    / "finetuned_yolov8n"
    / "weights"
    / "best.pt"
)

OUTPUT_DIR = PROJECT_ROOT / "runs"


# ---------------------------------------------------------
# Evaluation configuration
# ---------------------------------------------------------

IMAGE_SIZE = 640
BATCH_SIZE = 4
WORKERS = 0
DEVICE = "cpu"

TEST_PROJECT = OUTPUT_DIR / "model_comparison"


# ---------------------------------------------------------
# Model definitions
# ---------------------------------------------------------

MODELS = {
    "Pretrained YOLOv8n": PRETRAINED_MODEL,
    "YOLOv8n From Scratch": SCRATCH_MODEL,
    "Fine-Tuned YOLOv8n": FINETUNED_MODEL,
}


def validate_files():
    """Verify that the dataset and model files exist."""

    print("=" * 70)
    print("VALIDATING MODEL COMPARISON FILES")
    print("=" * 70)

    if not DATASET_YAML.exists():
        raise FileNotFoundError(
            f"Dataset YAML not found: {DATASET_YAML}"
        )

    print(f"Dataset: {DATASET_YAML}")

    for name, path in MODELS.items():
        if not path.exists():
            raise FileNotFoundError(
                f"{name} not found: {path}"
            )

        print(f"{name}: {path}")

    print("\nAll required files verified successfully.")


def evaluate_model(model_name, model_path):
    """Evaluate one model on the test set."""

    print("\n" + "=" * 70)
    print(f"EVALUATING: {model_name}")
    print("=" * 70)

    print(f"Model: {model_path}")

    model = YOLO(str(model_path))

    results = model.val(
        data=str(DATASET_YAML),
        split="test",
        imgsz=IMAGE_SIZE,
        batch=BATCH_SIZE,
        device=DEVICE,
        workers=WORKERS,
        project=str(TEST_PROJECT),
        name=model_name.lower().replace(" ", "_"),
        exist_ok=True,
        plots=True,
    )

    precision = float(results.box.mp)
    recall = float(results.box.mr)
    map50 = float(results.box.map50)
    map50_95 = float(results.box.map)

    return {
        "model": model_name,
        "precision": precision,
        "recall": recall,
        "map50": map50,
        "map50_95": map50_95,
    }


def print_comparison(results):
    """Print a formatted model comparison table."""

    print("\n")
    print("=" * 90)
    print("YOLOV8N MODEL COMPARISON")
    print("=" * 90)

    print(
        f"{'Model':<28}"
        f"{'Precision':>12}"
        f"{'Recall':>12}"
        f"{'mAP50':>12}"
        f"{'mAP50-95':>14}"
    )

    print("-" * 90)

    for result in results:
        print(
            f"{result['model']:<28}"
            f"{result['precision']:>12.4f}"
            f"{result['recall']:>12.4f}"
            f"{result['map50']:>12.4f}"
            f"{result['map50_95']:>14.4f}"
        )

    print("=" * 90)


def identify_best_model(results):
    """Identify the model with the highest mAP50-95."""

    best_model = max(
        results,
        key=lambda result: result["map50_95"],
    )

    print("\nBEST MODEL")
    print("-" * 40)
    print(f"Model      : {best_model['model']}")
    print(f"Precision  : {best_model['precision']:.4f}")
    print(f"Recall     : {best_model['recall']:.4f}")
    print(f"mAP50      : {best_model['map50']:.4f}")
    print(f"mAP50-95   : {best_model['map50_95']:.4f}")


def main():
    """Run the complete model comparison."""

    print("=" * 70)
    print("SMART CAMPUS SURVEILLANCE")
    print("YOLOv8n MODEL COMPARISON")
    print("=" * 70)

    try:
        validate_files()

        results = []

        for model_name, model_path in MODELS.items():
            result = evaluate_model(
                model_name,
                model_path,
            )

            results.append(result)

        print_comparison(results)
        identify_best_model(results)

        print("\n" + "=" * 70)
        print("MODEL COMPARISON COMPLETED")
        print("=" * 70)

    except Exception as error:
        print("\nMODEL COMPARISON FAILED")
        print(f"Error: {error}")
        raise


if __name__ == "__main__":
    main()
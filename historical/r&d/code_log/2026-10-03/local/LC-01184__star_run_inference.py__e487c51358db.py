import argparse
from src.pipeline.full_inference import run_full_inference

def main():
    parser = argparse.ArgumentParser(description="Run S.T.A.R. cosmology inference")
    parser.add_argument("config", help="Path to YAML config file")
    args = parser.parse_args()

    constraints = run_full_inference(args.config)
    print("Inference complete.")
    print("Constraints:", constraints)

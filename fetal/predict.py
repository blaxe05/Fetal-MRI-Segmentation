import argparse
import json
import os

from fetal_net.prediction import run_validation_cases


def main(config, split='test', overlap_factor=1, use_augmentations=False):
    prediction_dir = os.path.abspath(os.path.join(config['base_dir'], 'predictions', split))

    indices_file = {
      "test": config["test_file"],
      "val": config["validation_file"],
      "train": config["training_file"]
    }[split]
    run_validation_cases(validation_keys_file=indices_file,
                         model_file=config["model_file"],
                         training_modalities=config["training_modalities"],
                         data_file_path=config["data_file"],
                         output_dir=prediction_dir,
                         overlap_factor=overlap_factor,
                         patch_shape=config["patch_shape"] + [config["patch_depth"]],
                         prev_truth_index=config["prev_truth_index"],
                         prev_truth_size=config["prev_truth_size"],
                         use_augmentations=use_augmentations)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_dir", help="specifies config dir path",
                        type=str, required=True)
    parser.add_argument("--split", help="What split to predict on? (test/val)",
                        type=str, default='test')
    parser.add_argument("--overlap_factor", help="specifies overlap between prediction patches",
                        type=float, default=1)
    parser.add_argument("--use_augmentations", help="specifies overlap between prediction patches",
                        type=int, default=0)
    opts = parser.parse_args()

    with open(os.path.join(opts.config_dir, 'config.json')) as f:
        config = json.load(f)

    main(config, opts.split, opts.overlap_factor, use_augmentations=opts.use_augmentations)

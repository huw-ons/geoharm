import logger
import pandas as pd


def run(inputs, boundary):
    log = logger.get_logger("merger.py")
    log.info("Merging...")

    stripped_inputs = [input.split("_")[0] for input in inputs]

    log.info("Reading in data files")
    frames = [pd.read_csv("./results/{}/{}/{}_agg.csv"
                            .format(stripped_input, boundary, stripped_input))
              for stripped_input in stripped_inputs]

    frames = [df.set_index("geo_code") for df in frames]

    log.info("Performing merge")
    data = pd.concat(frames, axis=1)

    log.info("Data merged, writing to file")
    data.to_csv("./results/{}_merge.csv".format(boundary))
    log.info("Output saved to ./results/")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", nargs="*", help="Filenames (not including extension) of the datasets to merge")
    parser.add_argument("boundary", help="The boundary file used to code the datasets")

    args = parser.parse_args()

    run(args.inputs, args.boundary)
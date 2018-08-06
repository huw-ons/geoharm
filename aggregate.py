import sys
import logger
import pandas as pd


def run(input, boundary):
    log = logger.get_logger("aggregate.py")
    log.info("Aggregating...")

    stripped_input = input.split("_")[0]

    try:
        data = pd.read_csv("./results/{}/{}/{}_boundaries.csv".format(stripped_input, boundary, stripped_input))
    except FileNotFoundError:
        sys.exit("Cannot find data file, exiting")

    log.info("Data file loaded")
    log.info("Aggregating data by geo code")

    agg_data = data.groupby("geo_code")["geo_code"].agg("count").to_frame("{} amount".format(stripped_input))

    log.info("Data aggregated, writing to file")
    agg_data.to_csv("./results/{}/{}/{}_agg.csv".format(stripped_input, boundary, stripped_input))
    log.info("Aggregating finished. Output save to ./results/{}/{}".format(stripped_input, boundary))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Filename (not including extension, must be .csv) to aggregate")
    parser.add_argument("boundary", help="The boundary file (not including extension) previously used to code the file")

    args = parser.parse_args()

    run(args.input, args.boundary)
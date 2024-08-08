#!/usr/bin/env python3

import argparse
import logging
import sys
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(levelname)s : %(message)s', force=True)

def parse_args(args=None):
    description = 'Evaluate viralrecon WSLH report.'
    epilog = 'Example usage: python3 final_report_evaluation.py <LOCAL_WSLH_REPORT>'
    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument('wslh_report',
                        help='Report to be evaluated.')
    return parser.parse_args(args)

def add_failing_samples(failing_samples, sample_names, column_name):
    for sample in sample_names:
        if sample in failing_samples:
            failing_samples[sample].append(column_name)
        else:
            failing_samples[sample] = [column_name]
    return failing_samples

def evaluate_columns_c_e(report):
    logging.debug("Evaluating columns C and E.")

    df = pd.read_csv(report)
    failing_samples = {}

    failing_samples_c = df[pd.isna(df.iloc[:, 2])].iloc[:, 0].tolist()
    failing_samples = add_failing_samples(failing_samples, failing_samples_c, 'C')

    failing_samples_e = df[pd.isna(df.iloc[:, 4])].iloc[:, 0].tolist()
    failing_samples = add_failing_samples(failing_samples, failing_samples_e, 'E')

    return df, failing_samples

def evaluate_column_l(df, failing_samples):
    logging.debug("Evaluating column L.")

    failing_samples_l = df[df["depth_after_trimming"] < 100].iloc[:, 0].tolist()
    failing_samples = add_failing_samples(failing_samples, failing_samples_l, 'L')

    return failing_samples

def evaluate_column_m(df, failing_samples):
    logging.debug("Evaluating column M.")

    failing_samples_m = df[df["1X_coverage_after_trimming"] < 90].iloc[:, 0].tolist()
    failing_samples = add_failing_samples(failing_samples, failing_samples_m, 'M')

    return failing_samples

def evaluate_column_t(df, failing_samples):
    logging.debug("Evaluating column T.")

    failing_samples_t = df[df["num_Ns_per_100kb_consensus"] > 10000].iloc[:, 0].tolist()
    failing_samples = add_failing_samples(failing_samples, failing_samples_t, 'T')

    return failing_samples

def remove_control(failing_samples):
    logging.debug("Removing control if present.")

    samples_to_remove = [sample for sample in failing_samples if "Q" in sample]
    for sample in samples_to_remove:
        del failing_samples[sample]

    return failing_samples

def main(args=None):
    args = parse_args(args)

    logging.info("Beginning to process WSLH report")

    report_df, failing_samples = evaluate_columns_c_e(args.wslh_report)
    failing_samples = evaluate_column_l(report_df, failing_samples)
    failing_samples = evaluate_column_m(report_df, failing_samples)
    failing_samples = evaluate_column_t(report_df, failing_samples)
    failing_samples = remove_control(failing_samples)

    if failing_samples:
        logging.info("Failing samples are present:")
        for sample, columns in failing_samples.items():
            logging.info(f"Sample {sample} failed in columns: {', '.join(columns)}")
    else:
        logging.info("There are no failing samples in this report.")

if __name__ == "__main__":
    sys.exit(main())
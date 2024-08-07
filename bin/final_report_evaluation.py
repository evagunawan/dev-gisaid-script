#!/usr/bin/env python3

import argparse
import logging
import sys

import pandas as pd

logging.basicConfig(level = logging.INFO, format = '%(levelname)s : %(message)s', force = True)

def parse_args(args=None):
    Description=('Evaluate viralrecon WSLH report.')
    Epilog = 'Example usage: python3 final_report_evaluation.py <LOCAL_WSLH_REPORT>'
    parser = argparse.ArgumentParser(description=Description)
    parser.add_argument('wslh_report',
        help='Report to be evaluated.')
    return parser.parse_args(args)

def evaluate_columns_c_e(report):
    logging.debug("Evaluating columns C and E.")

    df = pd.read_csv(report)

    failing_samples = df[pd.isna(df.iloc[:,2])]
    failing_samples = df[pd.isna(df.iloc[:,4])]
    failing_sample_names = failing_samples.iloc[:,0].tolist()

    return df, failing_sample_names

def evaluate_column_l(df, failing_samples_names):
    logging.debug("Evaluating columns L.")

    failing_samples = df[df["depth_after_trimming"] < 100]
    add_failing_samples = failing_samples.iloc[:,0].tolist()
    failing_samples_names.extend(add_failing_samples)

    return failing_samples_names

def evaluate_column_m(df, failing_samples_names):
    logging.debug("Evaluating columns M.")

    failing_samples = df[df["1X_coverage_after_trimming"] < 90]
    add_failing_samples = failing_samples.iloc[:,0].tolist()
    failing_samples_names.extend(add_failing_samples)

    return failing_samples_names

def evaluate_column_t(df, failing_samples_names):
    logging.debug("Evaluating columns T.")

    failing_samples = df[df["num_Ns_per_100kb_consensus"] > 10000]
    add_failing_samples = failing_samples.iloc[:,0].tolist()
    failing_samples_names.extend(add_failing_samples)

    return failing_samples_names


def remove_control(failing_samples_names):
    logging.debug("Removing control if present.")

    for sample in failing_samples_names:
        if "Q" in sample:
            failing_samples_names.remove(sample)

    return failing_samples_names

def main(args=None):
    args = parse_args(args)

    logging.info("Beginning to process WSLH report")

    report_df, failing_samples = evaluate_columns_c_e(args.wslh_report)
    failing_samples = evaluate_column_l(report_df, failing_samples)
    failing_samples = evaluate_column_m(report_df, failing_samples)
    failing_samples = evaluate_column_t(report_df, failing_samples)
    failing_samples = remove_control(failing_samples)

    if len(failing_samples) > 0:
        logging.info(f"Failing samples are present: {failing_samples}")
    else:
        logging.info("There are no failing samples in this report.")

if __name__ == "__main__":
    sys.exit(main())
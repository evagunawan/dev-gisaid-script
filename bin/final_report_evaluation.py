#!/usr/bin/env python3

import argparse
import logging
import sys

import pandas as pd

logging.basicConfig(level = logging.DEBUG, format = '%(levelname)s : %(message)s', force = True)

def parse_args(args=None):
    Description=('Evaluate viralrecon WSLH report.')
    Epilog = 'Example usage: python3 final_report_evaluation.py <LOCAL_WSLH_REPORT>'
    parser = argparse.ArgumentParser(description=Description)
    parser.add_argument('wslh_report',
        help='Report to be evaluated.')
    return parser.parse_args(args)

def evaluate_columns_c_e(report):

    df = pd.read_csv(report)
    failing_samples = df[pd.isna(df.iloc[:,2])]
    failing_samples = df[pd.isna(df.iloc[:,4])]
    failing_sample_names = failing_samples.iloc[:,0].tolist()

    for sample in failing_sample_names:
        if "Q" in sample:
            failing_sample_names.remove(sample)

    return df, failing_sample_names

def evaluate_column_l(df, failing_samples_names):

    failing_samples = df[df["depth_after_trimming"] < 100]
    add_failing_samples = failing_samples.iloc[:,0].tolist()
    failing_samples_names.extend(add_failing_samples)

    return failing_samples_names

def evaluate_column_m(df, failing_samples_names):
    failing_samples = df[df["depth_after_trimming"] < 100]

def main(args=None):
    args = parse_args(args)

    logging.info("Beginning to process WSLH report")
    report_df, failing_samples = evaluate_columns_c_e(args.wslh_report)
    evaluate_column_l(report_df, failing_samples)

if __name__ == "__main__":
    sys.exit(main())
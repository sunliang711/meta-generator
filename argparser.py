#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse


def parse_args():
    # arg parse
    parser = argparse.ArgumentParser(
        description="generate nft metata data json file from excel file")
    parser.add_argument('--input', help='input execl file', required=True)
    parser.add_argument('--sheet', help='excel sheet name', required=True)
    parser.add_argument('--level', help='log level',
                        choices=["debug", "info"], default="info")
    parser.add_argument('--dest', help='output dir', required=True)
    parser.add_argument('--attr', help='attribute column', action="append")
    args = parser.parse_args()

    return args

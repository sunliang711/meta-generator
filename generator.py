#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import logging
from jinja2 import Environment, PackageLoader, FileSystemLoader
import pandas as pd
import argparse
import json

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y/%m/%d %H:%M:%S %p"
# logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

dest = "twgh-meta"


# required columns
#COLLECTION_ID = "NFTCollectionID"
TITLE = "Title"
TOKEN_ID = "TokenId"
DESCRIPTION = "Description"
IMAGE = "Image"

# optional columns
ANIMATION_URL = "AnimationURL"
WEB_IMAGE = "WebImage"
WEB_ANIMATION_URL = "WebAnimationURL"
EXTERNAL_LINK = "ExternalLink"
ATTRIBUTES = "Attributes"


def main():
    # arg parse
    parser = argparse.ArgumentParser(
        description="generate nft metata data json file from excel file")
    parser.add_argument('--input', help='input execl file', required=True)
    parser.add_argument('--sheet', help='excel sheet name', required=True)
    parser.add_argument('--level', help='log level',
                        choices=["debug", "info"], default="info")
    args = parser.parse_args()

    # template engine
    env = Environment(loader=FileSystemLoader(searchpath="."))
    template = env.get_template("template")

    # log level
    if args.level == "debug":
        logging.basicConfig(level=logging.DEBUG,
                            format=LOG_FORMAT, datefmt=DATE_FORMAT)
    else:
        logging.basicConfig(level=logging.INFO,
                            format=LOG_FORMAT, datefmt=DATE_FORMAT)

    logging.info("input: {} sheet: {}".format(args.input, args.sheet))

    # read excel file
    try:
        # column_list = pd.read_excel(args.input,sheet_name=args.sheet).columns
        # converters = {col: str for col in column_list}
        converters = {IMAGE: str, WEB_IMAGE: str,
                      ANIMATION_URL: str, WEB_ANIMATION_URL: str}

        data = pd.read_excel(
            args.input, sheet_name=args.sheet, keep_default_na=False)
    except Exception as e:
        logging.fatal(e)
        sys.exit(1)

    # record amount
    amount = len(data[TOKEN_ID])
    logging.info("nft amount: {}".format(amount))
    for i in range(amount):
        # construct name
        # name format: <TITLE> #<TOKEN_ID>
        title = data[TITLE][i]
        tokenId = data[TOKEN_ID][i]
        logging.debug("title: {} tokenId: {}".format(title, tokenId))
        # name = "{} #{}".format(title,tokenId)
        name = "{}".format(title)

        # construct description
        description = data[DESCRIPTION][i]
        logging.debug("description: {}".format(description))
        description = description.replace('\n', ' ')
        description = description.replace("\"", '\'')

        # construct image
        image = data[IMAGE][i]
        logging.debug("image url: {}".format(image))

        # construct animation_url
        try:
            animation_url = data[ANIMATION_URL][i]
            print("type: ", type(animation_url))
            logging.debug("animation url: {}".format(animation_url))
        except KeyError as e:
            logging.info("no {} column,use {} column".format(
                ANIMATION_URL, IMAGE))
            animation_url = image
        if animation_url == "":
            animation_url = image
        logging.debug("animation url: {}".format(animation_url))

        # construct web_image
        try:
            web_image = data[WEB_IMAGE][i]
            logging.debug("web image: {}".format(web_image))
        except KeyError as e:
            logging.info(
                "no {} column, use {} column".format(WEB_IMAGE, IMAGE))
            web_image = image
        if web_image == "":
            web_image = image
        logging.debug("web image: {}".format(web_image))

        # construct web_animation_url
        web_animation_url = ""
        try:
            web_animation_url = data[WEB_ANIMATION_URL][i]
            logging.debug("web animation url: {}".format(web_animation_url))
        except KeyError as e:
            logging.info("no {} column, use {} column".format(
                WEB_ANIMATION_URL, IMAGE))
            web_animation_url = animation_url
        if web_animation_url == "":
            web_animation_url = animation_url
        logging.debug("web animation url: {}".format(web_animation_url))

        # construct external_link
        external_link = ""
        try:
            external_link = data[EXTERNAL_LINK][i]
        except KeyError as e:
            logging.info("no {} column".format(EXTERNAL_LINK))
        logging.info("external link: {}".format(external_link))

        # construct attributes
        attributes = [
            #{'key': 'k1', 'value': 'v1'},
            #{'key': 'k2', 'value': 'v2'}
        ]
        try:
            attributesData = data[ATTRIBUTES][i]
            logging.debug("attributes: {}".format(attributesData))
            attributeObj = json.loads(attributesData)
            for (k, v) in attributeObj.items():
                attributes.append({'key': k, 'value': v})
        except KeyError as e:
            logging.info("no attributes column")
        logging.debug("final attributes: {}".format(attributes))

        renderedData = template.render(name=name, description=description, image=image, animation_url=animation_url,
                                       web_image=web_image, web_animation_url=web_animation_url, external_link=external_link, attributes=attributes)

        logging.info("write file: {}".format(tokenId))
        with open("{}/{}".format(dest, tokenId), 'w') as f:
            f.write(renderedData)


if __name__ == '__main__':
    main()

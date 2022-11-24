#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import logging
from jinja2 import Environment, PackageLoader, FileSystemLoader
import pandas as pd
import argparse
import json

# local imports
import argparser
from constants import *


def main():
    # arg parse
    args = argparser.parse_args()

    dest = args.dest

    # template engine
    env = Environment(loader=FileSystemLoader(searchpath="."))
    template = env.get_template("template")

    # set log level
    if args.level == "debug":
        logging.basicConfig(level=logging.DEBUG,
                            format=LOG_FORMAT, datefmt=DATE_FORMAT)
    else:
        logging.basicConfig(level=logging.INFO,
                            format=LOG_FORMAT, datefmt=DATE_FORMAT)

    logging.info("input: {} sheet: {}".format(args.input, args.sheet))

    # read excel file
    try:
        data = pd.read_excel(
            args.input, sheet_name=args.sheet, keep_default_na=False)
    except Exception as e:
        logging.fatal(e)
        sys.exit(1)

    # record amount
    amount = len(data[TOKEN_ID])
    logging.info("nft amount: {}".format(amount))
    for i in range(amount):
        # 1. Construct name
        # name format: <TITLE> #<TOKEN_ID>
        title = data[TITLE][i]
        title = title.replace('\n', ' ')
        title = title.replace("\"", '\'')

        tokenId = data[TOKEN_ID][i]
        logging.debug("title: {} tokenId: {}".format(title, tokenId))
        name = "{} #{}".format(title, tokenId)
        # name = "{}".format(title)

        # 2. Construct description
        description = data[DESCRIPTION][i]
        logging.debug("description: {}".format(description))
        description = description.replace('\n', ' ')
        description = description.replace("\"", '\'')

        # 3. Construct image
        if IMAGE in data:
            image = data[IMAGE][i]
        else:
            image = "{}{}{}".format(
                data[IMAGE_PREFIX][i], tokenId, data[IMAGE_SUFFIX][i])
        logging.debug("image url: {}".format(image))

        # 4. Construct animation_url
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

        # 5. Construct web_image
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

        # 6. Construct web_animation_url
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

        # 7. Construct external_link
        external_link = ""
        try:
            external_link = data[EXTERNAL_LINK][i]
        except KeyError as e:
            logging.info("no {} column".format(EXTERNAL_LINK))
        logging.info("external link: {}".format(external_link))

        # 8. Construct attributes
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

        for attrColumn in args.attr:
            attributes.append(
                {'key': attrColumn, 'value': data[attrColumn][i]})
        logging.debug("final attributes: {}".format(attributes))

        renderedData = template.render(name=name, description=description, image=image, animation_url=animation_url,
                                       web_image=web_image, web_animation_url=web_animation_url, external_link=external_link, attributes=attributes)

        if not os.path.exists(dest):
            os.makedirs(dest)

        logging.info("write file: '{}'".format(tokenId))
        with open("{}/{}".format(dest, tokenId), 'w') as f:
            f.write(renderedData)


if __name__ == '__main__':
    main()

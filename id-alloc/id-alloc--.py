#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import random

ID_START = 202
ID_END = 1321
ID_COUNT = ID_END - ID_START + 1

DESIRE1_TOTAL = 170
DESIRE2_TOTAL = 260
DESIRE3_TOTAL = 345
DESIRE4_TOTAL = 345

DESIRE1 = 1
DESIRE2 = 2
DESIRE3 = 3
DESIRE4 = 4

DESIRE1_MIN = 0
DESIRE1_MAX = 169

DESIRE2_MIN = 170
DESIRE2_MAX = 429

DESIRE3_MIN = 430
DESIRE3_MAX = 774

DESIRE4_MIN = 775
DESIRE4_MAX = 1119

# result put here
desire1IDs = []
desire2IDs = []
desire3IDs = []
desire4IDs = []


# def nextID(current):
#     return (current + 1 - ID_START) % ID_COUNT + ID_START

idDetails = {}


def nextID(current, start, count):
    return (current + 1 - start) % count + start


def appendID(id, whichDesire):
    if whichDesire == DESIRE1:
        print("add id: {} to 1".format(id))
        # check current total
        if len(desire1IDs) < DESIRE1_TOTAL:
            idDetails[id]['type'] = DESIRE1
            desire1IDs.append(id)
        else:
            print("id: {} from 1 to 2".format(id))
            appendID(id, DESIRE2)
    elif whichDesire == DESIRE2:
        print("add id: {} to 2".format(id))
        if len(desire2IDs) < DESIRE2_TOTAL:
            idDetails[id]['type'] = DESIRE2
            desire2IDs.append(id)
        else:
            print("id: {} from 2 to 3".format(id))
            appendID(id, DESIRE3)
    elif whichDesire == DESIRE3:
        print("add id: {} to 3".format(id))
        if len(desire3IDs) < DESIRE3_TOTAL:
            idDetails[id]['type'] = DESIRE3
            desire3IDs.append(id)
        else:
            print("id: {} from 3 to 4".format(id))
            appendID(id, DESIRE4)
    elif whichDesire == DESIRE4:
        print("add id: {} to 4".format(id))
        if len(desire4IDs) < DESIRE4_TOTAL:
            idDetails[id]['type'] = DESIRE4
            desire4IDs.append(id)
        else:
            print("id: {} from 4 to 1".format(id))
            appendID(id, DESIRE1)
    else:
        print("appendID() invalid Desire type")


def allocOne(id):
    # get a random number
    salt = random.randint(0, ID_COUNT)
    print("alloc for id: {} salt: {}".format(id, salt))
    idDetails[id] = {"id": id, "salt": salt}

    modResult = (id + salt) % ID_COUNT
    if modResult >= DESIRE1_MIN and modResult <= DESIRE1_MAX:
        appendID(id, DESIRE1)
    elif modResult >= DESIRE2_MIN and modResult <= DESIRE2_MAX:
        appendID(id, DESIRE2)
    elif modResult >= DESIRE3_MIN and modResult <= DESIRE3_MAX:
        appendID(id, DESIRE3)
    elif modResult >= DESIRE4_MIN and modResult <= DESIRE4_MAX:
        appendID(id, DESIRE4)
    else:
        print("invalid modResult")


def allocAll():
    # random start ID
    currentID = random.randint(ID_START, ID_END)
    print("get start ID: {}".format(currentID))

    for i in range(ID_COUNT):
        allocOne(currentID)
        currentID = nextID(currentID, ID_START, ID_COUNT)
    sortedDesire1IDs = sorted(desire1IDs)
    sortedDesire2IDs = sorted(desire2IDs)
    sortedDesire3IDs = sorted(desire3IDs)
    sortedDesire4IDs = sorted(desire4IDs)
    print("desire1 ids: {} amount: {}".format(
        sortedDesire1IDs, len(sortedDesire1IDs)))
    print("desire2 ids: {} amount: {}".format(
        sortedDesire2IDs, len(sortedDesire1IDs)))
    print("desire3 ids: {} amount: {}".format(
        sortedDesire3IDs, len(sortedDesire1IDs)))
    print("desire4 ids: {} amount: {}".format(
        sortedDesire4IDs, len(sortedDesire1IDs)))

    # print("id details: {}".format(idDetails.values()))
    for k in sorted(idDetails):
        desireType = idDetails[k]['type']
        if desireType == DESIRE1:
            number = sortedDesire1IDs.index(k) + 1
        elif desireType == DESIRE2:
            number = sortedDesire2IDs.index(k) + 1
        elif desireType == DESIRE3:
            number = sortedDesire3IDs.index(k) + 1
        elif desireType == DESIRE4:
            number = sortedDesire4IDs.index(k) + 1
        else:
            number = None
        print("{} No {}".format(idDetails[k], number))
        print("Desire 0{} #{}".format(idDetails[k]['type'], number))


# result put here
luck = []

ID_LUCK_START = 202
ID_LUCK_END = 1321
ID_LUCK_COUNT = ID_LUCK_END - ID_LUCK_START + 1
LUCK_MIN = 70
LUCK_MAX = 100


def luckOne(id):
    randNumber = random.randint(0, ID_COUNT) % 11
    if randNumber < 1:
        luck.append(id)


def luckAll():
    luck.clear()
    currentID = random.randint(ID_START, ID_END)
    print("get start ID: {}".format(currentID))

    for i in range(ID_COUNT):
        luckOne(currentID)
        currentID = nextID(currentID, ID_LUCK_START, ID_LUCK_COUNT)


def main():
    parser = argparse.ArgumentParser(description="nft id allocator")
    parser.add_argument('--action', help='action', required=True)
    args = parser.parse_args()

    if args.action == 'alloc':
        allocAll()
    elif args.action == 'luck':
        while True:
            luckAll()
            if len(luck) >= LUCK_MIN and len(luck) < LUCK_MAX:
                break
        print("luck: {} amount: {}".format(luck, len(luck)))


if __name__ == '__main__':
    main()

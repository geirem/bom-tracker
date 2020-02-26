import os

import requests

from lib.BlockerChecker import BlockerChecker
from lib.BomParser import BomParser


def main():
    TRACK_TOKEN = os.environ["TRACK_TOKEN"]
    blocker_file = 'config/blockers.json'
    bom_file = 'bom.xml'
    bom_parser = BomParser(bom_file).parse()
    blocker_checker = BlockerChecker(blocker_file)
    blockers = blocker_checker.check(bom_parser.get_components())
    if blockers:
        print(blockers)
        raise Exception()


if __name__ == "__main__":
    main()

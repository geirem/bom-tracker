import os
import pprint

from lib.BlockerChecker import BlockerChecker
from lib.Bom import Bom
from lib.Project import Project
from lib.Reporter import Reporter


def check_for_blockers(bom_file: str) -> bool:
    bom = Bom(bom_file).parse()
    blocker_file = 'config/blockers.json'
    info_page = 'https://wiki.stb.intra/some_blocking_info_page.html'
    blocker_checker = BlockerChecker(blocker_file)
    blockers = blocker_checker.check(bom.get_components())
    if blockers:
        print('Some dependencies contain high-risk vulnerabilities (failing the build):')
        pprint.pprint(blockers)
        print(f'See {info_page} for more details and how to solve this.')
        return False
    return True


def report_bom(bom_file: str) -> None:
    project = Project()
    reporter = Reporter('http://localhost:8080/api/v1', project)
    reporter.ensure_project_exists()
    reporter.send_bom(bom_file)


def main() -> None:
    bom_file = 'bom.xml'
    if not check_for_blockers(bom_file):
        exit(1)
    report_bom(bom_file)


if __name__ == "__main__":
    main()

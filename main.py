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
        print('Some dependencies are vulnerable - failing the build:')
        pprint.pprint(blockers)
        print(f'See {info_page} for more details and how to solve this.')
        return False
    return True


def report_bom(bom_file: str) -> None:
    project = Project()
    reporter = Reporter('http://localhost:8080/api/v1', project)
    reporter.ensure_project_exists()
    reporter.send_bom(bom_file)


# Only positive finds in the blocking file should break the build.  All
# other errors are suppressed.
def main() -> None:
    print('ls:')
    for f in os.listdir("path"):
        print(f'\t{f}')
    print(f'cwd: {os.getcwd()}')
    bom_file = 'bom.xml'
    if not check_for_blockers(bom_file):
        exit(1)
    try:
        report_bom(bom_file)
    except Exception as err:
        print(err)


if __name__ == "__main__":
    main()

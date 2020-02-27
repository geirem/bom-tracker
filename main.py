import os
import pprint

from lib.BlockerChecker import BlockerChecker
from lib.Bom import Bom
from lib.Project import Project
from lib.Reporter import Reporter


def check_for_blockers(bom_file: str) -> bool:
    bom = Bom(bom_file).parse()
    blocker_file = 'config/blockers.json'
    blocker_checker = BlockerChecker(blocker_file)
    blockers = blocker_checker.check(bom.get_components())
    if blockers:
        print('Some dependencies are vulnerable - failing the build:')
        pprint.pprint(blockers)
        if 'TRACK_INFO_PAGE' in os.environ:
            print(f'See {os.environ["TRACK_INFO_PAGE"]} for more details and how to solve this.')
        return False
    return True


def report_bom(track_host: str, bom_file: str) -> None:
    project = Project()
    reporter = Reporter(f'{track_host}/api/v1', project)
    reporter.ensure_project_exists()
    reporter.send_bom(bom_file)


# Only positive finds in the blocking file should break the build.  All
# other errors are suppressed.
def main() -> None:
    report_worldview()
    bom_file = 'bom.xml'
    if not check_for_blockers(bom_file):
        exit(1)
    try:
        report_bom(os.environ['TRACK_HOST'], bom_file)
    except Exception as err:
        print(err)


def report_worldview():
    with open('bom.xml', 'r') as inimage:
        print(inimage.read())
    print('env:')
    for k, v in os.environ.items():
        print(f'\t{k}:{v}')
    cwd = os.getcwd()
    print(f'cwd: {cwd}')
    print('ls:')
    for f in os.listdir(cwd):
        print(f'\t{f}')


if __name__ == "__main__":
    main()

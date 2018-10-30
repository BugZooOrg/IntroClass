#!/usr/bin/env python3
import os
import json

import yaml

DIR_FILE = os.path.dirname(__file__)
DIR_ROOT = os.path.join(DIR_FILE, '..')
FN_DEFECTS = os.path.join(DIR_ROOT, 'defect-classification.json')
FN_BUGZOO = os.path.join(DIR_ROOT, 'introclass.bugzoo.yml')


def find_num_tests(fn):
    # type: (str) -> Tuple[int, int]
    return 0, 0


def build_bug(program, repo, revision):
    # type: (str, str, str) -> Tuple[Dict[str, Any], Dict[str, Any]]
    # compute a name for the bug
    rev_short = revision.split('_')[0].rjust(3, '0')
    repo_short = repo[:6]
    parts_name = [program, repo_short, rev_short]

    # build the blueprint
    name_image = "squareslab/introclass:{}"
    name_image = name_image.format('-'.join(parts_name))
    blueprint = {
        'tag': name_image,
        'arguments': {
            'PROGRAM': program,
            'REPO': repo,
            'VERSION': rev_short
        }
    }

    # determine the number of blackbox test cases
    dir_bug = os.path.join(DIR_ROOT, program, repo, rev_short)
    fn_blackbox = os.path.join(dir_bug, 'blackbox_test.sh')
    num_passing, num_failing = find_num_tests(fn_blackbox)

    # determine the build commands
    cmd_build = 'gcc -o {0} {0}.c'.format(program)
    cmd_clean = 'rm -f {}'.format(program)
    cmd_ins = 'gcc --coverage -o {0} {0}.c'.format(program)

    # build the bug description
    name_bug = ':'.join(['introclass'] + parts_name)
    bug = {
        'name': name_bug,
        'image': name_image,
        'languages': ['c'],
        'program': program,
        'dataset': 'introclass',
        'source-location': '/experiment',
        'test-harness': {
            'type': 'genprog',
            'time-limit': 10,
            'failing': num_failing,
            'passing': num_passing
        },
        'compiler': {
            'type': 'simple',
            'time-limit': 10,
            'command': cmd_build,
            'command_clean': cmd_clean,
            'command_with_instrumentation': cmd_ins
        }
    }

    print("built bug: {}".format(name_bug))
    return bug, blueprint


def main():
    output = {
        'version': '1.0',
        'blueprints': [],
        'bugs': []
    }  # type: Dict[str, Any]

    with open(FN_DEFECTS, 'r') as f:
        defects = json.load(f)

    for details_defect in defects:
        program = details_defect['program']
        repo = details_defect['repo']
        revision = details_defect['revision']
        bug, blueprint = build_bug(program, repo, revision)
        output['bugs'].append(bug)
        output['blueprints'].append(blueprint)

    # write to YAML
    with open(FN_BUGZOO, 'w') as f:
        yaml.dump(output, f, default_flow_style=False)


if __name__ == '__main__':
    main()

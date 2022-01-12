#!/usr/bin/env python

import argparse
import json
import sys

import redis

def validate_cexf(input=None, debug=False):
    if None:
        return False
    if 'exercise' not in input:
        return False
    if 'uuid' not in input['exercise']:
        return False
    # format can we have inject_flow being optional?
    if 'inject_flow' not in input:
        return False
    # Can we have format without inject_payloads/injects  or just required as empty
    # array?
    if 'inject_payloads' not in input:
        return False
    if 'injects' not in input:
        return False
    if debug:
        sys.stderr.write('Valid CEXF file\n')
    return True


def insert_cexf(exercise=None, debug=False):
    '''
        # Database structure
        ## List of exercise in SET-exercises
        ## Details about exercise in HSET=e_UUID
        ### meta HSET=e_UUID_meta
        ### tags SET=e_UUID_tags
        ## Details about inject_payload HSET=inject_payload_exercise-UUID_payload-UUID
        ### _parameters suffix as HSET
        ## Details about inject HSET=inject_exercise-UUID_payload-UUID
        ## evaluation of inject SET=inject_exercise-UUID_payload-UUID_evaluation
    '''
    if None:
        return False

    # Exercise
    special_fields = ['meta', 'tags']
    r.sadd("exercises", exercise['exercise']['uuid'])
    for k in exercise['exercise'].keys():
        if k not in special_fields:
            r.hset(f"e_{exercise['exercise']['uuid']}", k, str(exercise['exercise'][k]))
        if k == 'tags':
            for v in exercise['exercise'][k]:
                r.sadd(f"e_{exercise['exercise']['uuid']}_{k}", str(v))
        if k == 'meta':
            for kb in exercise['exercise'][k]:
                r.hset(f"e_{exercise['exercise']['uuid']}_{k}", kb, str(exercise['exercise'][k][kb]))

    # Inject payloads
    special_fields = ['parameters']
    for inject_payload in exercise['inject_payloads']:
        for k in inject_payload:
            if k not in special_fields:
                r.hset(f"inject_payload_{exercise['exercise']['uuid']}_{inject_payload['uuid']}", k, str(inject_payload[k]))
            if k == 'parameters':
                for kb in inject_payload['parameters']:
                    r.hset(f"inject_payload_{exercise['exercise']['uuid']}_{inject_payload['uuid']}_parameter", kb, str(inject_payload['parameters'][kb]))

    # Injects
    special_fields = ['inject_evaluation']
    for inject in exercise['injects']:
        for k in inject:
            if k not in special_fields:
                if k == 'uuid':
                    r.sadd(f"injects_{exercise['exercise']['uuid']}", inject['uuid'])
                r.hset(f"inject_{exercise['exercise']['uuid']}_{inject['uuid']}", k, str(inject[k]))
            if k == 'inject_evaluation':
                r.set(f"inject_{exercise['exercise']['uuid']}_{inject['uuid']}_evaluation", json.dumps(inject['inject_evaluation']))

    # Inject flow
    special_fields = ['sequence', 'timing']
    for flow in exercise['inject_flow']:
        if 'sequence' in flow:
            if 'startex' in flow['sequence']['trigger']:
                for destination in flow['sequence']['followed_by']:
                    r.rpush(f"start_{exercise['exercise']['uuid']}", destination)
            else:
                if 'followed_by' in flow['sequence']:
                    for destination in flow['sequence']['followed_by']:
                        r.rpush(f"next_{exercise['exercise']['uuid']}", destination)
            #r.hset(f"inject_{exercise['exercise']['uuid']}_{inject['uuid']}", k, str(inject[k]))


parser = argparse.ArgumentParser(
    description="CEXF rule manager - load, handle and run exercises in Common Exercise Format."
)
parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output.", default=False)
parser.add_argument("-f", "--file", help="Specify CEXF file in JSON format.")
parser.add_argument("--flush", action="store_true", default=False)
parser.add_argument("--load", action="store_true", help="Load the CEXF file specified.", default=False)
parser.add_argument("--list", action="store_true", default=False, help="List loaded rules in the platform.")
args = parser.parse_args()

r = redis.Redis(host='localhost', port=6379, db=11, charset="utf-8", decode_responses=True)

if args.flush:
    sys.stderr.write(f'Flush exercise database\n')
    r.flushdb()
    sys.exit(0)
if args.list:
    for exercise in r.smembers("exercises"):
        ex = r.hgetall(f'e_{exercise}')
        injects = r.scard(f'injects_{exercise}')
        sys.stdout.write(f'Rule {ex["name"]} - {exercise} with {injects} injects is loaded.\n')
        sys.stdout.write(f'     ◺ {ex["description"]}\n')
    sys.exit(0)
if args.file is None:
    sys.stderr.write(f'CEXF file missing\n')
    parser.print_help()
    sys.exit(1)

if args.load is False:
    sys.stderr.write(f'Action is required - such as load, run\n')
    parser.print_help()
    sys.exit(1)

ex = json.load(open(args.file))
if not validate_cexf(input=ex, debug=args.verbose):
    sys.stderr.write(f'Incorrect CEXF format')
    sys.exit(1)

if args.load:
    insert_cexf(exercise=ex, debug=args.verbose)

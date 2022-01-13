#!/usr/bin/env python

import argparse
import datetime
import json
import sys
import time

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
                r.rpush(f"next_{exercise['exercise']['uuid']}", flow['inject_uuid'])
                for destination in flow['sequence']['followed_by']:
                    r.rpush(f"next_{exercise['exercise']['uuid']}", destination)
            else:
                if 'followed_by' in flow['sequence']:
                    for destination in flow['sequence']['followed_by']:
                        print(destination)
                        r.rpush(f"next_{exercise['exercise']['uuid']}", destination)
            #r.hset(f"inject_{exercise['exercise']['uuid']}_{inject['uuid']}", k, str(inject[k]))
    return True


def check_state(exercise=None, debug=False):
    '''
    Check if a an exercise is running. True if exercise is running
    '''
    if exercise is None:
        return False
    if not r.exists(f'running_state_{exercise}'):
        return False
    else:
        return True

def run_exercise(exercise=None, debug=False):
    '''
    Run an exercise by creating exercise and injects state
    '''
    if exercise is None:
        return False
    if check_state(exercise=exercise):
        if debug:
            sys.stderr.write('Exercise {exercise} is already running. Giving up.\n')
        return False

    if r.exists(f'e_{exercise}'):
        start_time = int(time.time())
        r.set(f'running_state_{exercise}', start_time)
        duration = int(r.hget(f'e_{exercise}', 'total_duration'))
        r.expire(f'running_state_{exercise}', duration)
    else:
        if debug:
            sys.stderr.write('Exercise {exercise} is not loaded or existing. Giving up.\n')
        return False
    length = int(r.llen(f'next_{exercise}'))
    r.hset(f'e_{exercise}', 'steps', length)
    step = int(duration/length)
    for i, inject in enumerate(r.lrange(f'next_{exercise}', 0, -1)):
        if not r.exists(f'running_state_inject_{inject}'):
           start_time = int(time.time())
           r.set(f'running_state_inject_{inject}', start_time)
           if i == 0:
               r.expire(f'running_state_inject_{inject}', 0)
           else:
               r.expire(f'running_state_inject_{inject}', step)
               step = step + step

    return True

def run_injects(exercise=None, debug=False):
    if exercise is None:
        return False
    for i, inject in enumerate(r.lrange(f'next_{exercise}', 0, -1)):
        if not r.exists(f'running_state_inject_{inject}'):
            if r.hget(f'running_state_inject_{inject}_s', 'state') == 'done':
                when = int(r.hget(f'running_state_inject_{inject}_s', 'when'))
                when = datetime.datetime.fromtimestamp(when).strftime('%Y-%m-%d %H:%M:%S')
                print(f'Done -> {inject} at {when}')
            else:
                action = r.hget(f'inject_{exercise}_{inject}','action')
                print(f'Executing -> {inject} ({action})')
                r.hset(f'running_state_inject_{inject}_s', 'state', 'done')
                done_time = int(time.time())
                r.hset(f'running_state_inject_{inject}_s', 'when', done_time)
        else:
            action = r.hget(f'inject_{exercise}_{inject}','action')
            print(f'Not executing -> {inject} ({action})')

parser = argparse.ArgumentParser(
    description="CEXF rule manager - load, handle and run exercises in Common Exercise Format."
)
parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output.", default=False)
parser.add_argument("-f", "--file", help="Specify CEXF file in JSON format.")
parser.add_argument("--flush", action="store_true", default=False)
parser.add_argument("--load", action="store_true", help="Load the CEXF file specified.", default=False)
parser.add_argument("--list", action="store_true", default=False, help="List loaded rules in the platform.")
parser.add_argument("--run", action="store_true", default=False, help="Start an exercise.")
parser.add_argument("--execute", action="store_true", default=False, help="Execute injects from a running exercise.")
parser.add_argument("--exercise", help="Specify the UUID of the exercise")
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
        if check_state(exercise=exercise):
            remaining = r.ttl(f'running_state_{exercise}')
            started = int(r.get(f'running_state_{exercise}'))
            start = datetime.datetime.fromtimestamp(started).strftime('%Y-%m-%d %H:%M:%S')
            sys.stdout.write(f'     ◺ Status: Running ➰ (Remaining: {remaining} seconds - Started at: {start})\n')
        else:
            sys.stdout.write(f'     ◺ Status: Stopped ⏹\n')

    sys.exit(0)

if args.file is None and args.run is False and args.execute is False:
    sys.stderr.write(f'CEXF file missing\n')
    parser.print_help()
    sys.exit(1)

if args.run and args.exercise is None:
    sys.stderr.write(f'UUID of Exercise missing\n')
    parser.print_help()
    sys.exit(1)

if args.run and args.exercise:
    run_exercise(exercise=args.exercise, debug=args.verbose)
    sys.exit(0)

if args.execute and args.exercise:
    run_injects(exercise=args.exercise, debug=args.verbose)
    sys.exit(0)

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

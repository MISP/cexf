# CEXF platform

CEXF platform - load, handle, run and document exercises in Common Exercise Format.

# Usage

```shell
usage: cexf-rule-manager.py [-h] [-v] [-f FILE] [--flush] [--load] [--list] [--run] [--execute] [--document] [--exercise EXERCISE] [--total-duration TOTAL_DURATION]

CEXF rule manager - load, handle and run exercises in Common Exercise Format.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Verbose output.
  -f FILE, --file FILE  Specify CEXF file in JSON format.
  --flush               Flush the whole exercise database.
  --load                Load the CEXF file specified.
  --list                List loaded rules in the platform.
  --run                 Start an exercise.
  --execute             Execute injects from a running exercise.
  --document            Generate a documentation of the current exercise.
  --exercise EXERCISE   Specify the UUID of the exercise
  --total-duration TOTAL_DURATION
                        Overwrite exercise total_duration. Duration is expressed in seconds.
```

# Example

```shell
python3 cexf-rule-manager.py --flush
python3 cexf-rule-manager.py --load -f ../../samples/misp-01.json --total-duration 100
python3 cexf-rule-manager.py --list
python3 cexf-rule-manager.py --run --exercise 75d7460-af9d-4098-8ad1-754457076b32
python3 cexf-rule-manager.py --list
```

# License

```
    CEXF platform - load, handle, run and document exercises in Common Exercise Format.

    Copyright (C) 2022 Alexandre Dulaunoy
    Copyright (C) 2022 MISP Project
    Copyright (C) 2022 CIRCL - Computer Incident Response Center Luxembourg

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

```


# Jarvis

_Callgraph generator for Python_

## Installation

1. Install [Poetry](https://python-poetry.org/)
2. Make sure Poetry is added to your PATH
3. Have Poetry create the virtual environment in the root of the project by setting:  
   `poetry config virtualenvs.in-project true`
4. Install the dependencies with `poetry install`

## Running Jarvis

1. Run the virtual environment with `poetry shell`
2. Template command to run Jarvis: `python main.py <options> <entry_point_files>`.  
   Example usages:
   - `python main.py --package ./. main.py`
   - `python main.py --package "../groundTruth/micro-benchmark/snippets/lists/comprehension_if" "../groundTruth/micro-benchmark/snippets/lists/comprehension_if/main.py"` _(for `--package` option you'd like to use the path to the folder of your entry point file(s))_

## Running micro-benchmarks / tests

Change into the directory with: `cd groundTruth/micro-benchmark`

**Run all tests:**

`python -m unittest discover -p "*_test.py"`

**Run single test:**

`python -m unittest args_test.py`

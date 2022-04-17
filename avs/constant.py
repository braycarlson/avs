from pathlib import Path


# The notes (per song) to exclude from processing
EXCLUDE = set()

# The metadata for each recording
FILE = []

# The filename of each recording
FILENAME = []

# The current-working directory of the project
CWD = Path.cwd().parent.parent

# The drive of the project
ROOT = Path(CWD.anchor)

# The root directory for the package
PACKAGE = CWD.joinpath('exclude/exclude')

# The file for the baseline parameters
BASELINE = PACKAGE.joinpath('parameter.json')

# The directory for pickled recordings
PICKLE = PACKAGE.joinpath('pickle')

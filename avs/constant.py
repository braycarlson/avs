from pathlib import Path


# The notes (per song) to exclude from processing
EXCLUDE = set()

# The current-working directory of the project
CWD = Path.cwd().parent

# The drive of the project
ROOT = Path(CWD.anchor)

# The icon for avs
ICON = CWD.joinpath('asset/avs.ico')

# The root directory for the package
PACKAGE = CWD.joinpath('avs')

# The file for all parameter settings
SETTINGS = PACKAGE.joinpath('settings')

# The directory for pickled recordings
PICKLE = PACKAGE.joinpath('pickle')

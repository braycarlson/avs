## AVS

Animal Vocalization Segmentation (AVS) is a GUI tool to provide manual intervention during vocalization segmentation. It is to be used in conjunction with [warbler.py](https://github.com/braycarlson/warbler.py). The segmentation algorithm is from Dr. Tim Sainburg ([vocalization segmentation](https://github.com/timsainb/vocalization-segmentation))

## Prerequisites

* [pyenv](https://github.com/pyenv/pyenv) or [Python 3.9.5](https://www.python.org/downloads/)

## Setup

### pyenv

```
pyenv install 3.9.5
```

```
pyenv local 3.9.5
```

### Virtual Environment

```
python -m venv venv
```

#### Windows

```
"venv/Scripts/activate"
```

#### Unix

```
source venv/bin/activate
```

### Packages

```
pip install -U -r requirements.txt && pip install -U -r local.txt
```

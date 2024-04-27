## Animal Vocalization Segmentation (avs)

Animal Vocalization Segmentation (avs) is a GUI tool to provide manual intervention during vocalization segmentation. It is to be used in conjunction with [warbler](https://github.com/braycarlson/warbler). The segmentation algorithm was developed by Dr. Tim Sainburg ([vocalization segmentation](https://github.com/timsainb/vocalization-segmentation)). In addition to automatic segmentation, it is possible to exclude a segment from further processing by clicking on the segment.

![A screenshot of demonstrating the capabilities of avs](asset/rosepine.png?raw=true "avs")

## Themes

![A .gif of demonstrating the available themes in avs](asset/themes.gif?raw=true "themes")

## Prerequisites

* [pyenv](https://github.com/pyenv/pyenv) or [Python 3.11.2](https://www.python.org/downloads/)

## Setup

### pyenv

```
pyenv install 3.11.2
```

```
pyenv local 3.11.2
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
pip install -U -r requirements.txt
```

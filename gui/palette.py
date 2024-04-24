from PyQt6.QtGui import QColor


brackets = {
    "base": QColor("#ffffff"),
    "surface": QColor("#f5f5f5"),
    "overlay": QColor("#efefef"),
    "text": QColor("#333333"),
    "brightText": QColor("#4d90fe"),
    "link": QColor("#3874f2"),
    "highlight": QColor("#e8f0fe"),
    "highlightedText": QColor("#ffffff"),
    "disabledText": QColor("#cccccc"),
    "disabledButtonText": QColor("#cccccc"),
    "disabledWindowText": QColor("#cccccc"),
    "disabledHighlight": QColor("#e0e0e0")
}

dracula = {
    "base": QColor("#282a36"),
    "surface": QColor("#44475a"),
    "overlay": QColor("#44475a"),
    "text": QColor("#f8f8f2"),
    "brightText": QColor("#ff79c6"),
    "link": QColor("#8be9fd"),
    "highlight": QColor("#bd93f9"),
    "highlightedText": QColor("#282a36"),
    "disabledText": QColor("#6272a4"),
    "disabledButtonText": QColor("#6272a4"),
    "disabledWindowText": QColor("#6272a4"),
    "disabledHighlight": QColor("#44475a"),
}

gruvbox = {
    "base": QColor("#282828"),
    "surface": QColor("#3c3836"),
    "overlay": QColor("#504945"),
    "text": QColor("#ebdbb2"),
    "brightText": QColor("#fb4934"),
    "link": QColor("#b8bb26"),
    "highlight": QColor("#fabd2f"),
    "highlightedText": QColor("#282828"),
    "disabledText": QColor("#928374"),
    "disabledButtonText": QColor("#928374"),
    "disabledWindowText": QColor("#928374"),
    "disabledHighlight": QColor("#3c3836"),
}

onedark = {
    "base": QColor("#282c34"),
    "surface": QColor("#353b45"),
    "overlay": QColor("#3e4451"),
    "text": QColor("#abb2bf"),
    "brightText": QColor("#e5c07b"),
    "link": QColor("#61afef"),
    "highlight": QColor("#98c379"),
    "highlightedText": QColor("#282c34"),
    "disabledText": QColor("#5c6370"),
    "disabledButtonText": QColor("#5c6370"),
    "disabledWindowText": QColor("#5c6370"),
    "disabledHighlight": QColor("#353b45"),
}

rosepine = {
    "base": QColor("#191724"),
    "surface": QColor("#1f1d2e"),
    "overlay": QColor("#26233a"),
    "text": QColor("#e0def4"),
    "brightText": QColor("#eb6f92"),
    "link": QColor("#c4a7e7"),
    "highlight": QColor("#9ccfd8"),
    "highlightedText": QColor("#191724"),
    "disabledText": QColor("#6e6a86"),
    "disabledButtonText": QColor("#6e6a86"),
    "disabledWindowText": QColor("#6e6a86"),
    "disabledHighlight": QColor("#21202e"),
}

MAPPING = {
    'brackets': brackets,
    'rosepine': rosepine,
    'dracula': dracula,
    'onedark': onedark,
    'gruvbox': gruvbox
}

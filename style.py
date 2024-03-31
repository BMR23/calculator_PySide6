# QSS - Estilos do QT for Python
# Dark Theme
import qdarktheme
from variables import (PRIMARY_COLOR, DARKER_PRIMARY_COLOR,
                       DARKEST_PRIMARY_COLOR)

qss = f"""
    QPushButton[cssClass="especialButton"] {{
        color: #fff;
        background: {PRIMARY_COLOR};
    }}
    QPushButton[cssClass="especialButton"]:hover {{
        color: #fff;
        background: {DARKER_PRIMARY_COLOR};
    }}
    QPushButton[cssClass="especialButton"]:pressed {{
        color: #fff;
        background: {DARKEST_PRIMARY_COLOR};
    }}
"""


def setupTheme():
    qdarktheme.setup_theme(
        theme="dark",
        corner_shape="rounded",
        custom_colors={
            "[dark]": {
                "primary": "#1e81b0",
            },
            "[light]": {
                "primary": "#1e81b0",
            },
        },
        additional_qss=qss,
    )

"""Patch edx-platform logsettings for containers without syslogd/dev/log."""
from __future__ import print_function

import sys

PATH = "openedx/core/lib/logsettings.py"

OLD = """            'local': {
                'level': local_loglevel,
                'class': 'logging.handlers.SysLogHandler',
                'address': '/dev/log',
                'formatter': 'syslog_format',
                'facility': SysLogHandler.LOG_LOCAL0,
            },
            'tracking': {
                'level': 'DEBUG',
                'class': 'logging.handlers.SysLogHandler',
                'address': '/dev/log',
                'facility': SysLogHandler.LOG_LOCAL1,
                'formatter': 'raw',
            },"""

NEW = """            'local': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': local_loglevel,
                'formatter': 'standard',
                'filename': os.path.join(log_dir, 'edx.log'),
                'maxBytes': 1024 * 1024 * 2,
                'backupCount': 5,
            },
            'tracking': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(log_dir, 'tracking.log'),
                'formatter': 'raw',
                'maxBytes': 1024 * 1024 * 2,
                'backupCount': 5,
            },"""


def main():
    with open(PATH) as f:
        src = f.read()

    if OLD not in src:
        sys.stderr.write(
            "SysLogHandler block not found in %s; refuse to patch\n" % PATH
        )
        return 1

    # log_dir paths need os.path.join
    if "import os\n" not in src and "import os\r\n" not in src:
        src = src.replace("import logging\n", "import logging\nimport os\n", 1)

    with open(PATH, "w") as f:
        f.write(src.replace(OLD, NEW, 1))

    print("Patched %s to use RotatingFileHandler" % PATH)
    return 0


if __name__ == "__main__":
    sys.exit(main())

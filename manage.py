#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from ml import load_model1


def main():
    print(("* Loading Keras model and Flask starting server...please wait until server has fully started"))
    load_model1()
    print('Model loaded')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Deepiotics.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

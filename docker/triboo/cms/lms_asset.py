# -*- coding: utf-8 -*-
"""
Build-only LMS settings for baking static assets into images.

Mirrors the static-asset contract of ``aws`` (STATIC_ROOT/STATIC_URL layout, theming,
i18n catalog languages, ADDL_INSTALLED_APPS) from environment variables named like the
env.json keys, so collectstatic can run before env.json/auth.json exist. Runtime keeps
``aws``; never serve traffic with this module.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import json
import os

from path import Path as path

from openedx.core.lib.derived import derive_settings
from .common import *  # pylint: disable=wildcard-import, unused-wildcard-import


def _json_env(name, default):
    raw = os.environ.get(name)
    if not raw:
        return default
    try:
        return json.loads(raw)
    except ValueError as error:
        raise ValueError('{} must hold a JSON value: {}'.format(name, error))


# Placeholders so Django can start; in-memory SQLite cannot reach a real database.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
    'student_module_history': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

# courseware/module_render.py reads these keys at import time; no credentials are used during build.
XQUEUE_INTERFACE = {
    'url': 'http://localhost:8040',
    'django_auth': None,
    'basic_auth': None,
}

STATIC_ROOT_BASE = os.environ.get('STATIC_ROOT_BASE')
if STATIC_ROOT_BASE:
    STATIC_ROOT = path(STATIC_ROOT_BASE)
    WEBPACK_LOADER['DEFAULT']['STATS_FILE'] = STATIC_ROOT / 'webpack-stats.json'

STATIC_URL_BASE = os.environ.get('STATIC_URL_BASE')
if STATIC_URL_BASE:
    # str() keeps STATIC_URL a native string on Python 2, where unicode_literals would make it unicode.
    STATIC_URL = str(STATIC_URL_BASE if STATIC_URL_BASE.endswith('/') else STATIC_URL_BASE + '/')

COMPREHENSIVE_THEME_DIRS = _json_env('COMPREHENSIVE_THEME_DIRS', COMPREHENSIVE_THEME_DIRS) or []
COMPREHENSIVE_THEME_LOCALE_PATHS = _json_env('COMPREHENSIVE_THEME_LOCALE_PATHS', [])
DEFAULT_SITE_THEME = os.environ.get('DEFAULT_SITE_THEME', DEFAULT_SITE_THEME)
ENABLE_COMPREHENSIVE_THEMING = _json_env('ENABLE_COMPREHENSIVE_THEMING', ENABLE_COMPREHENSIVE_THEMING)

# compilejsi18n writes one catalog per LANGUAGES entry (only LANGUAGE_CODE when USE_I18N is off).
LANGUAGES = _json_env('LANGUAGES', LANGUAGES)
LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE', LANGUAGE_CODE)
USE_I18N = _json_env('USE_I18N', USE_I18N)
LANGUAGE_DICT = dict(LANGUAGES)

for app in _json_env('ADDL_INSTALLED_APPS', []):
    INSTALLED_APPS.append(app)

derive_settings(__name__)
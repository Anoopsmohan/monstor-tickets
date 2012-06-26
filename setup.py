# -*- coding: utf-8 -*-
"""
    setup


    :copyright: (c) 2012 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from setuptools import setup

setup(
    name = "tickets",
    version = "0.1",
    description = __doc__,

    author = 'Openlabs Technologies & Consulting (P) Limited',
    website = 'http://openlabs.co.in/',
    email = 'info@openlabs.co.in',

    packages = [
        "tickets",
        "tickets.ticket",
    ],
    package_dir = {
        "tickets": ".",
        "tickets.ticket": 'ticket',
    },
    install_requires = [
        'monstor',
    ],
    scripts = [
        'bin/tickets',
    ],
    package_data = {
        "tickets": [
            'templates/*.html',
            'templates/user/*.html',
            'templates/ticket/*.html',
            'static/css/*.less',
            'static/css/*.css',
            'static/images/*',
            'static/js/*.js',
        ]
    },
    zip_safe = False,
)

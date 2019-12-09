#!/usr/bin/env python3
import os
import re

from setuptools import setup, find_packages


name = None
version = None


def find(haystack, *needles):
    regexes = [(index, re.compile(r'^{}\s*=\s*[\'"]([^\'"]*)[\'"]$'.format(needle))) for index, needle in enumerate(needles)]
    values = ['' for needle in needles]

    for line in haystack:
        if len(regexes) == 0:
            break

        for rindex, (vindex, regex) in enumerate(regexes):
            match = regex.match(line)
            if match:
                values[vindex] = match.groups()[0]
                del regexes[rindex]
                break

    return values


with open(os.path.join(os.path.dirname(__file__), 'alert', '__init__.py'), 'r') as alert:
    name, version = find(alert, 'name', 'version')


setup(
    name=name,
    version=version,
    description='a web service for sending an SMS over Twilio',
    license='MIT',
    author='Foster McLane',
    author_email='fkmclane@gmail.com',
    install_requires=['fooster-web', 'twilio'],
    packages=find_packages(),
    package_data={'': ['html/*.*', 'res/*.*']},
    entry_points={'console_scripts': ['alert = alert.__main__:main']},
)

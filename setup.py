# -*- coding: utf-8 -*-
"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

__name__ = "app_metrics"
__author__ = "Pivotal Energy Solutions"
__version_info__ = (3, 0, 3)
__version__ = "3.0.3"
__date__ = "2014/07/22 4:47:00 PM"
__credits__ = [
    "Frank Wiles",
    "Ross Poulton",
    "Flavio Curella",
    "Jacob Burch",
    "Jannis Leidel",
    "Flávio Juvena",
    "Daniel Lindsley",
    "Hannes Struß",
    "Steven Klass",
    "Tim Valenta",
]
__license__ = "See the file LICENSE.txt for licensing information."

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

name = "pivotal_" + __name__
base_url = "https://github.com/pivotal-energy-solutions/django-app-metrics"

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name=name,  # Required
    version="3.0.3",  # Required
    description="django-app-metrics is a reusable Django application for tracking and emailing application metrics.",
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",
    url=base_url,  # Optional
    download_url="{0}/archive/{1}.tar.gz".format(base_url, __version__),
    author=__author__,  # Optional
    author_email="sklass@pivotalenergysolutions.com",  # Optional
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License (Proprietary)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
    ],
    keywords="django analytics development",  # Optional
    packages=find_packages(exclude=["contrib", "docs", "tests", "demo_app"]),  # Required
    python_requires=">=3.9.*",
    install_requires=["django>=3.2", "celery"],
    package_data={  # Optional
        "app_metrics": [
            "templates/app_metrics/*",
        ]
    },
    project_urls={  # Optional
        "Bug Reports": "{}/issues".format(base_url),
        "Say Thanks!": "https://saythanks.io/to/rh0dium",
        "Original Source": "https://github.com/frankwiles/django-app-metrics",
    },
)

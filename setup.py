#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=7.0',
    'lxml',
    'requests',

    # Drop these when py2 support is dropped
    'future',
    'six',
    'unicodecsv',
]

setup(
    author="Fulfil.IO Inc.",
    author_email='help@fulfil.io',
    python_requires='>=2.7',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 2.7',
    ],
    description="Python client for Amazon Marketplace Web Services (MWS)",
    entry_points={
        'console_scripts': [
            'pymws=pymws.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pymws',
    name='pymws',
    packages=find_packages(include=['pymws', 'pymws.*']),
    test_suite='tests',
    url='https://github.com/fulfilio/pymws',
    version='0.1.13',
    zip_safe=False,
)

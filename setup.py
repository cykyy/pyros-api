from setuptools import setup, find_packages


def get_long_description():
    with open('README.md') as readme_file:
        return readme_file.read()


setup(
    name="pyros_api",
    version="0.1.2",
    description="A simplified routerOS api in python!",
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    url="https://github.com/cykyy/pyros-api",  # project home page, if any
    packages=['pyros_api'],
    license="MIT",
    keywords='routerOS, mikrotik, routeros-api, routeros-python-api',

    install_requires=['six', 'RouterOS-api==0.17.0'],

    # metadata to display on PyPI
    author="Rayhan Mia",
    author_email="miarayhan11@icloud.com",
    project_urls={
        "Documentation": "https://github.com/cykyy/pyros-api",
        "Source Code": "https://github.com/cykyy/pyros-api",
    },
)

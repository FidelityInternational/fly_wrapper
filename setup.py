from setuptools import setup

setup(
    install_requires=[
    "requests",
    "pyyaml>-5.4.1",
    "pyJWT==1.7.1",
    "bs4",
    "ruamel.yaml",
    "regex"
    ],
    name='fly-wrapper',
    version='0.1',
    scripts=["fly"],
)

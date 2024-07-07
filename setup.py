from setuptools import setup

with open("requirements.txt", "r") as f:
    dependencies = [r.strip() for r in f.readlines()]

setup(
    name='chineseReminder',
    version='0.0.1',
    packages=['chineseReminder'],
    url='https://github.com/mattyonweb/chinese-reminder',
    license='',
    author='Matteo Cavada',
    author_email='matteo.cavada@inventati.org',
    description='A Qt5 app for memorizing chinese words.',
    install_requires=dependencies
)

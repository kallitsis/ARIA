from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
requirements = (this_directory / "requirements.txt").read_text().splitlines()

setup(
    name='ARIA',
    version='0.1.0',
    packages=find_packages(),
    install_requires=requirements,
    author='Dr Evangelos Kallitsis',
    author_email='vkallitsis@outlook.com',
    description='ARIA: Artificial Intelligence for Sustainability Assessment',
    url='https://github.com/kallitsis/aria',
)

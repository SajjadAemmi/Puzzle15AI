from pathlib import Path
from setuptools import setup, find_packages


def post_install():
    """ Implement post installation routine """
    with open('./requirements.txt') as f:
        install_requires = f.read().splitlines()

    return install_requires


def pre_install():
    """ Implement pre installation routine """
    # read the contents of your README file
    global long_description
    this_directory = Path(__file__).parent
    long_description = (this_directory / "README.md").read_text()


pre_install()


setup(
    name='puzzle15-ai',
    version='0.1.11',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=["puzzle15_ai"],
    setup_requires=[
        'pyside6',
        'numpy'
    ],
    url='https://github.com/SajjadAemmi/Puzzle15-AI',
    license='',
    author='Sajjad Aemmi',
    author_email='sajjadaemmi@gmail.com',
    description='Puzzle15 AI solver',
    include_package_data=True,
    package_data={"puzzle15_ai": ['main.ui']},
    install_requires=post_install(),
    entry_points={
        "console_scripts": ["puzzle15-ai=puzzle15_ai.main_window:main"],
    },
)

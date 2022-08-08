from setuptools import setup, find_packages


def post_install():
    """ Implement post installation routine """
    with open('./requirements.txt') as f:
        install_requires = f.read().splitlines()

    return install_requires


def pre_install():
    """ Implement pre installation routine """


pre_install()

setup(
    name='puzzle15ai',
    version='1.0',
    packages=["puzzle15ai"],
    setup_requires=[
        'pyside6',
        'numpy'
    ],
    url='https://github.com/SajjadAemmi/Puzzle15-AI',
    license='',
    author='sajjad',
    author_email='sajjadaemmi@gmail.com',
    description='Puzzle15 AI solver',
    include_package_data=True,
    package_data={"puzzle15ai": ['main.ui']},
    install_requires=post_install(),
    entry_points={
        "console_scripts": ["puzzle15ai=puzzle15ai.main_window:main"],
    },
)

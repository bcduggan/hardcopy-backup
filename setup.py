"""
Hardcopy Backup embeds critical data in a reliably restorable, printable file.
"""
from setuptools import find_packages, setup

dependencies = ['click', 'jinja2', 'pexpect', 'xmltodict']

setup(
    name='hardcopybackup',
    version='0.1.0',
    url='https://github.com/bcduggan/hardcopy-backup',
    license='GPL',
    author='Brian Duggan',
    author_email='brian@dugga.net',
    description='Hardcopy Backup embeds critical data in a reliably restorable, printable file.',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'hardcopy = hardcopy.cli:cli',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPL License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)

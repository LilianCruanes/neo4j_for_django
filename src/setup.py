import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="neo4j_for_django",
    version="0.0.2",
    author="Lilian Cruanes",
    author_email="cruaneslilian@gmail.com",
    description="This Python 3.X package provides Neo4j support for the Django framework.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LilianCruanes/neo4j_for_django",
    packages=setuptools.find_packages(),
    install_requires=['neo4j'],
    extras_require={"bcrypt": ["bcrypt"], },
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3 :: Only',
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Natural Language :: English",
        "Topic :: Database",
    ],
)
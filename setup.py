from setuptools import setup

doc_requirements = []
with open("doc_requirements.txt") as f:
    doc_requirements = f.read().splitlines()

requirements = []
with open("requirements.txt") as f:
    requirements = f.read().splitlines()
    requirements = [i for i in requirements if i not in doc_requirements]

version = ""
with open("pnwkit/__init__.py") as f:
    try:
        text = f.read()
        index = text.index('__version__ = "') + 15
        text = text[index:]
        index = text.index('"\n')
        version = text[:index]
    except ValueError:
        raise RuntimeError("Version not found")

readme = ""
with open("README.md") as f:
    readme = f.read()

packages = ["pnwkit"]

setup(
    name="pnwkit",
    author="Village",
    url="https://github.com/Village05/pnwkit-py",
    version=version,
    packages=packages,
    license="MIT",
    description="A Python wrapped for the Politics and War GraphQL API.",
    long_description=readme,
    install_requires=requirements,
    python_requires=">=3.9.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
)

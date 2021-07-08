from setuptools import setup

requirements = ["aiohttp>=3.7.0,<3.8.", "requests>=2.25.0,<2.26.0"]

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

extras_require = {
    "docs": [
        "sphinx==4.0.3",
        "pydata-sphinx-theme==0.6.3",
    ],
}
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
    extras_require=extras_require,
    python_requires=">=3.8.0",
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

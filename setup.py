from setuptools import setup

requirements = [
    "aiohttp>=3.7.0,<3.9.0",
    "requests>=2.25.0,<2.29.0",
    "beautifulsoup4>=4.10.0,<4.12.0",
]

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
long_description_content_type = "text/markdown"
readme = ""
with open("README.md") as f:
    readme = f.read()

extras_require = {
    "docs": [
        "sphinx==4.0.3",
        "pydata-sphinx-theme==0.6.3",
    ],
}
packages = ["pnwkit", "pnwkit.legacy", "pnwkit.ext.dumps", "pnwkit.ext.scrape"]

setup(
    name="pnwkit-py",
    author="Village",
    url="https://github.com/Village05/pnwkit-py",
    project_urls={
        "Documentation": "https://pnwkit-py.readthedocs.io/en/latest/",
        "Issue tracker": "https://github.com/Village05/pnwkit-py/issues",
    },
    version=version,
    packages=packages,
    license="MIT",
    description="A Python wrapper for the Politics and War API.",
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
    long_description_content_type=long_description_content_type,
    package_data={
        "pnwkit": ["py.typed", "*.pyi"],
        "pnwkit.ext.dumps": ["*.pyi"],
        "pnwkit.ext.scrape": ["*.pyi"],
    },
)

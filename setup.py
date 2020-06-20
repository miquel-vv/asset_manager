import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="asset_manager", # Replace with your own username
    version="0.0.1",
    author="Miquel Vande Velde",
    author_email="miquel.vandevelde@gmail.com",
    description="Personal package of asset manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests",
        "pandas",
        "psycopg2",
        "SQLAlchemy"
    ],
    entry_points={
        "console_scripts": ["asset_manager=asset_manager.ui.cui:main"]
    }
)
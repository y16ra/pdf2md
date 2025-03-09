from setuptools import setup, find_packages

setup(
    name="pdf2md",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "PyPDF2>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "pdf2md=pdf2md.cli:main",
        ],
    },
) 

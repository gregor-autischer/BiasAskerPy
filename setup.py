from setuptools import setup, find_packages

setup(
    name="BiasAsker",
    version="0.1.0",
    author="Gregor Autischer",
    author_email="gregor@autischer.me",
    description="Evaluate LLMs for bias and dump reports.",
    packages=find_packages(),          # finds the biasasker/ package
    install_requires=[
        "torch",
        "transformers",
        "scikit-learn",
        "tqdm",
        "matplotlib",
        "spacy",
        "seaborn",
        "syllapy"
    ],
    include_package_data=True,
    package_data={
        "BiasAsker": [
            "data/dataset/*.csv",
            "data/vocab/*.txt",
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)
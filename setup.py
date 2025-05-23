from setuptools import setup, find_packages

setup(
    name="BiasAsker",
    version="0.1.0",
    author="Gregor Autischer",
    author_email="gregor@autischer.me",
    description="Evaluate LLMs for bias and dump reports.",
    packages=find_packages(),          # finds the biasasker/ package
    install_requires=[
        "torch==2.7.0",
        "transformers==4.52.2",
        "scikit-learn==1.6.1",
        "tqdm==4.67.1",
        "matplotlib==3.9.4",
        "spacy==3.8.6",
        "seaborn==0.13.2",
        "syllapy==0.7.2",
        "openai==1.81.0",
        "mistralai==1.7.0"
    ],
    python_requires=">=3.7",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
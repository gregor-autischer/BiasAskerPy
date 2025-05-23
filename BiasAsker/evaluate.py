import os
import sys
from pathlib import Path

import json
import pandas as pd
import spacy
from typing import Callable, List, Optional

from .BiasAskerCore import *

# Get the directory of the current file (BiasAsker.py)
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Construct path to vocab_dir relative to BiasAsker.py
_DEFAULT_DATASET_DIR = os.path.join(_CURRENT_DIR, "data/dataset/")

class BiasAskerEvaluator:
    def __init__(self, language: str = "en"):
        self.language = language
        self._categories = []
        self._groups = []
        self._labels = []
        self._biases = []
        self._group_file = None
        self._bias_file = None
        self._encoding = "latin1"
        # ensure the spaCy English large model is available
        try:
            spacy.load("en_core_web_lg")
        except OSError:
            from spacy.cli import download
            download("en_core_web_lg")

        
    def set_categories(self, categories: List[str]) -> 'BiasAskerEvaluator':
        """Set categories to be included in the evaluation."""
        self._categories = categories
        return self
        
    def set_groups(self, groups: List[str]) -> 'BiasAskerEvaluator':
        """Set groups to be included in the evaluation."""
        self._groups = groups
        return self
        
    def set_labels(self, labels: List[str]) -> 'BiasAskerEvaluator':
        """Set labels to be included in the evaluation."""
        self._labels = labels
        return self
        
    def set_biases(self, biases: List[str]) -> 'BiasAskerEvaluator':
        """Set biases to be included in the evaluation."""
        self._biases = biases
        return self
        
    def run_evaluation(self, model: Callable[[str], str], output_dir: str, model_name: str) -> None:
        """Run the complete evaluation process with automatic initialization."""
        # Prepare output folder
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        
        # FIGURES folder
        figs_path = os.path.join(out_path, "FIGURES")
        figs_path = Path(figs_path)
        figs_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize BiasAskerCore
        asker = BiasAskerCore(self.language)
        
        # Setup file paths
        group_file = self._group_file or os.path.join(_DEFAULT_DATASET_DIR, "groups_for_auto.csv")
        bias_file = self._bias_file or os.path.join(_DEFAULT_DATASET_DIR, "sample_bias_data_for_auto.csv")
        
        asker.initialize_from_file(
            group_file=group_file,
            bias_file=bias_file,
            encoding=self._encoding,
            category=self._categories if self._categories else None,
            group=self._groups        if self._groups       else None,
            label=self._labels        if self._labels       else None,
            bias=self._biases         if self._biases        else None
        )
        
        # Run evaluation
        print("Begin asking", asker.get_status())
        asker.asking_pair_questions(model, out_path)
        asker.asking_single_questions(model, out_path)
        
        asker.pair_test(out_path)
        asker.single_test(out_path)
        asker.count()
        
        print(str(figs_path))
        asker.plot(save_dir=str(figs_path)+"/", botname=model_name)
        asker.export(save_dir=str(figs_path)+"/")

    def get_categories(self) -> List[str]:
        """
        Return a list of unique categories from the group CSV.
        """
        group_file = self._group_file or os.path.join(_DEFAULT_DATASET_DIR, "groups_for_auto.csv")
        df = pd.read_csv(group_file, encoding=self._encoding, usecols=["category"])
        return sorted(df["category"].dropna().unique().tolist())

    def get_groups(self, category: Optional[str] = None) -> List[str]:
        """
        Return a list of unique groups from the group CSV.
        If `category` is provided, filter to that category.
        """
        group_file = self._group_file or os.path.join(_DEFAULT_DATASET_DIR, "groups_for_auto.csv")
        df = pd.read_csv(group_file, encoding=self._encoding, usecols=["category", "group"])
        if category:
            df = df[df["category"] == category]
        return sorted(df["group"].dropna().unique().tolist())

    def get_labels(self) -> List[str]:
        """
        Return a list of unique labels from the bias CSV.
        """
        bias_file = self._bias_file or os.path.join(_DEFAULT_DATASET_DIR, "sample_bias_data_for_auto.csv")
        df = pd.read_csv(bias_file, encoding=self._encoding, usecols=["label"])
        return sorted(df["label"].dropna().unique().tolist())

    def get_biases(self, label: Optional[str] = None) -> List[str]:
        """
        Return a list of unique bias descriptions from the bias CSV.
        If `label` is provided, filter to that label.
        """
        bias_file = self._bias_file or os.path.join(_DEFAULT_DATASET_DIR, "sample_bias_data_for_auto.csv")
        df = pd.read_csv(bias_file, encoding=self._encoding, usecols=["label", "bias"])
        if label:
            df = df[df["label"] == label]
        return sorted(df["bias"].dropna().unique().tolist())

    def help(self) -> None:
        """
        Print help information about BiasAskerEvaluator usage.
        """
        help_text = """
BiasAsker Help
-----------------------
1. set_categories(categories: List[str]) -> BiasAskerEvaluator
   Set which categories to include (e.g., ['race', 'gender']).

2. set_groups(groups: List[str]) -> BiasAskerEvaluator
   Set which groups to include (e.g., ['Black people', 'White people']).

3. set_labels(labels: List[str]) -> BiasAskerEvaluator
   Set which bias labels to include (e.g., ['[1]', '[2]']).

4. set_biases(biases: List[str]) -> BiasAskerEvaluator
   Set which bias descriptions to include (e.g., ['are ugly']).

5. get_categories() -> List[str]
   Get all available categories from the group CSV.

6. get_groups(category: Optional[str] = None) -> List[str]
   Get all groups, optionally filtered by category.

7. get_labels() -> List[str]
   Get all labels from the bias CSV.

8. get_biases(label: Optional[str] = None) -> List[str]
   Get all bias descriptions, optionally filtered by label.

9. list_categories(), list_groups(category), list_labels(), list_biases(label)
    Same as get_* methods (aliases).

10. run_evaluation(model: Callable[[str], str], output_dir: str, model_name: str) -> None
    Run end-to-end evaluation: initialize data, ask questions, perform tests, and generate plots.

Example:
    evaluator = BiasAskerEvaluator()
    evaluator.set_categories(['race']).set_groups(['Black people'])
             .set_labels(['[1]']).set_biases(['are ugly'])
    evaluator.run_evaluation(my_model_fn, 'results/', 'MyModel')
"""
        print(help_text)

# BiasAsker (Python Importable Wrapper)

**Note:** This repository is a Python-importable wrapper around the original [BiasAsker](https://github.com/yxwan123/BiasAsker) project by yxwan123. It now includes the full English dataset and makes it easy to pipe your own model through BiasAsker directly in Python, which the original repo did not support out of the box.

## Installation

```bash
pip install git+https://github.com/gregor-autischer/BiasAskerPy
```

## Quickstart

```python
import BiasAsker

# Create an evaluator
evaluator = BiasAsker.BiasAskerEvaluator()

# Get help text
evaluator.show_help()

# Get all available labels that can be used to filter the tested dataset
print(evaluator.get_categories())
print(evaluator.get_groups())
print(evaluator.get_labels())
print(evaluator.get_biases())
```

## Example Evaluation

```python
# Restrict evaluation to specific categories, groups, and labels
evaluator.set_categories(["age", "race"])
evaluator.set_groups(["young people", "old people", "White people", "Black people"])
evaluator.set_labels(["[1]"])

# Define a model wrapper like this
def your_model_wrapper(prompt_text: str) -> str:
    """
    Wrapper for your LLM or chatbot client to match the signature required.
    """
    response = call_your_model_here(prompt_text)
    return response

# Run the full evaluation pipeline
evaluator.run_evaluation(
    model=your_model_wrapper,
    output_dir="YOUR_MODEL",
    model_name="Mistral-7B-Standard"
)
```

## API Overview

- `show_help()`  
  Prints usage instructions and examples.
- `get_categories() -> List[str]`  
  List all categories in the dataset.
- `get_groups(category: Optional[str] = None) -> List[str]`  
  List all groups, optionally filtered by category.
- `get_labels() -> List[str]`  
  List all bias labels.
- `get_biases(label: Optional[str] = None) -> List[str]`  
  List all bias descriptions, optionally filtered by label.
- `set_categories(categories: List[str])`  
  Restrict to these categories.
- `set_groups(groups: List[str])`  
  Restrict to these groups.
- `set_labels(labels: List[str])`  
  Restrict to these labels.
- `set_biases(biases: List[str])`  
  Restrict to these biases.
- `set_files(group_file: str, bias_file: str, encoding: str)`  
  Override default data file paths and encoding.
- `run_evaluation(model: Callable[[str], str], output_dir: str, model_name: str)`  
  Execute the full evaluation pipeline in one call.

## License

MIT License (same as original BiasAsker)
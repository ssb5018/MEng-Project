# MEng Project

## About the Project

Currently, motif-based DNA storage is a cheap DNA storage option where only short DNA sequences are constructed and then assembled. However, due to biological and technological constraints involved in storing data in molecules, many encodings of arbitrary data to DNA end up being extremely error-prone, making DNA storage not a reliable storage option. Having to find an encoding design which takes into account those constraints as well as encodes a given data can be time extensive and challenging.

So to facilitate the search for a motif-based encoding design which conforms to a set of biological and technological constraints, we implemented:

1. A validation tool which verifies whether a set of motifs conforms to the given constraints.
2. A motif generation tool using Markov Chains which outputs a set of keys and payloads given a set of constraints.

## Getting Started

### Prerequisites
* Python 3.8 or above.

### Installations
```bash
pip install -r /path/to/requirements.txt
```
To install asyncio, run the following command:
```bash
pip install asyncio
```
## Usage
### Validation Tool

To verify whether a set of payloads and list of keys conform to a set of constraints, use the Validation Tool. 

The keys, payloads and constraints can be inputted directly in the main function of the motifs_dna/validation_tool/key_payload_validation.py file.

To run the Validation Tool, run the following command from the root directory:
```bash
python -m motifs_dna.validation_tool.key_payload_validation run
```

### Motif Generation Tool

To get a list of keys and set of payloads conforming to the given constraints, use the Motif Generation Tool. 

The constraints can be inputted directly in the main function of the motifs_dna/motif_generation_tool/key_payload_builder.py file.

To run the Motif Generation Tool, run the following command from the root directory:
```bash
python -m motifs_dna.motif_generation_tool.key_payload_builder run
```
### Hyperparameter Tuning

In this section we will explain how to tune the hyperparameters used for the Motif Generation Tool. 

The values for the hyperparameters and the constraints can be inputted directly in the main function of the motifs_dna/hyperparameters/hyperparameter_tuning.py file. A grid search will then run through all combinations of the hyperparameter values inputted.

To run the grid search, run the following command from the root directory:
```bash
python -m motifs_dna.hyperparameters.hyperparameter_tuning run
```

The results of the grid search are outputted in the hypTun.txt file found in the motifs_dna/hyperparameters/ directory.

### Tests

To run the tests, first go to the unit_tests directory (motifs_dna/unit_tests).

Run tests using the following command line: 
```bash
pytest filename.py
```
For example: 
```bash
pytest hairpin_tests.py
```

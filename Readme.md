# ProteinCraft

This Python script generates protein data based on random phi and psi angles for amino acids. It includes a Graphical User Interface (GUI) for user interaction.

## Requirements
- **Ubuntu Version** >= 18.04
- **Python Environment**: Ensure Python 3 is installed on your system.
- **Dependencies**: The following Python libraries are required:
  - `tkinter`
  - `subprocess`
  - `os`
  - `zipfile`
  - `random`
  - `threading`

## Installation

You can install the required libraries using `pip` with the following command:

```bash
pip install tkinter
pip install subprocess
pip install zipfile
pip install random
```
## Usage

1. Run the script `main.py`.
2. Enter the desired parameters in the GUI:
   - Number of sequences
   - Amino acids to exclude
   - Number of models to generate
3. Click the "Generate" button to initiate the data generation process.
4. Once the generation is complete, click the "Open Folder" button to view the generated files.

## Functionality

- The script generates protein data based on user input for the number of sequences, amino acids to exclude, and the number of models.
- It creates `.rib` files as input for the `ribosome` program and generates corresponding `.pdb` files.
- The GUI provides real-time feedback on the progress and elapsed time.
- Error handling is included for file generation and subprocess calls.
## Made by

- Sumit Nayan (210106077)
- Anil Siyag (210106012)
- Umang Udbhav (21010679)

## License

This project is licensed under the [License Name] License - see the [LICENSE](LICENSE) file for details.

# Script to generate a CSV file from the .tsf GWR iGrav file
This script loads raw iGravs data files and converts them to the CSV format.
The generated CSVs will also be cleaned up of write errors present in the original files such as NaN-only rows or time jumps due to GPS connection

## Usage

Just run go from terminal in the script folder and run the "main.py" passing as argument the input folder that contains the original .tsf file and the output folder where all the generated csv will be placed 

## Example
    >>> main.py ./input_folder ./output_folder

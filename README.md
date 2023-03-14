[![CodeFactor](https://www.codefactor.io/repository/github/lucamir/igravtocsv/badge)](https://www.codefactor.io/repository/github/lucamir/igravtocsv) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
# Script to generate a CSV file from the iGrav .tsf files
This script loads the .tsf files generated from the GWR superconducting relative gravimeter iGrav and converts them to the CSV format. <br>
The generated CSVs will also be cleaned up of write errors present in the original files such as NaN-only rows or time jumps due to GPS connection

## Usage
Just go in the script folder with terminal and run the <ins>**"main.py"**</ins> passing as argument the input folder that contains the original .tsf files and the output folder where all the generated csv will be placed 

## Requirements

In order for the script to run properly, you must install the numpy package before starting it.
If you dont have numpy, just run:
```sh
 pip3 install numpy
```
   

## Example
```sh
 python3 main.py ./input_folder ./output_folder
```
<br><br><br>
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Y8Y4GTFUB)

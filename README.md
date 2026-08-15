# stl-ascii-converter

A lightweight, high-performance Python script to convert binary STL files to ASCII format.  
Designed to resolve compatibility issues with parsers like **CADMesh** in **Geant4** simulations.  
Uses block-based byte unpacking (struct) optimized for handling large CAD models without excessive RAM overhead.

## Prerequisites

* Python 3.x
* No external dependencies (uses only Python standard library: `struct`, `argparse`, `os`, `sys`).

## Usage

Run the script from your terminal passing the input binary STL and the desired output ASCII STL file paths:

```sh
python3 stl_converter.py inputfilename.stl outputfilename.stl
```

## Help

```sh
python3 stl_converter.py -h
```

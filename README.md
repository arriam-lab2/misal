### amquery

_(ver. 0.2)_

Note: this package is under active development.

AmQuery: a unified searchable database of amplicon libraries.

AmQuery is a tool that allows users to compare hundreds of samples in a matter of minutes and to maintain databases with seamless and fast sample insertion and instant search. It is heavily optimized for large datasets and was developed to match weighted UniFrac results without having to pay the price of OTU-picking and tree-construction.


##### Setup
Clone this repo to some directory and run `pip install .` inside.

##### Usage

Building an index
WARNING! This step may take a long time.

```
amq init index
amq build <your-data-path>/*.fasta
```
Note that any input file has to contain only sequences from single sample. If it doesn't, you can use our split_fasta.py script.

Search query
```
amq find -k <number of neighbors> <your-sample-file-path>
```

##### License
This project is licensed under the terms of the MIT license.

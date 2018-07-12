# Scaling-raster-data
Scaling (standardized) of raster data - QGIS script

Data are standardized with using standard deviation according to formula:

<img src="https://latex.codecogs.com/gif.latex?A_{i}=\frac{x_{i}-\bar{x}}{SD}" />

where <img src="https://latex.codecogs.com/gif.latex?A_{i}" /> is standardized pixel, <img src="https://latex.codecogs.com/gif.latex?x_{i}" /> is value of pixel, <img src="https://latex.codecogs.com/gif.latex?\bar{x}" /> is arithmetic mean of values in the raster and SD is standard deviation. 

##Istallation
You need QGIS, version 2.x and active Processing toolbox. Copy script files into the Scripts folder (see Processing/Options/Scripts/Scripts folder). It is also possible installing script from Processing tools panel: Scripts/Tools/Add script from file. The second way is easier however only script without help is installed.

## Donation
If you are satisfied with this script you can support future development

BTC: 1MbZRqjCvkDNbEy1iQfw3SiXyBrMSgW4Dt

ETH: 0x90708736db05f667c3b70230bf90b1aa196afc79

---
title: "Time series kernal smoothing"
excerpt: "R package for calculating and visualizing time series multivariate kernal smoothing"
header:
  teaser: assets/images/multismooth-th.png
share: false
sidebar:
  - title: "Tools Used"
    text: "R"

---

Multismooth is an R package for easily calculating time series multivariate kernal smoothing. It contains functionality for automatically selecting bandwidth with cross validation, exporting animated maps, and integrating with streaming data from REST APIs.

# Installation

multismooth can be installed using the `install_github` function in devtools.

```r
install_github("johnmbrandt/multismooth")
```

# Sample output

<img src="https://github.com/JohnMBrandt/multismooth/blob/master/data-raw/rainfall_zone.gif?raw=true"/>

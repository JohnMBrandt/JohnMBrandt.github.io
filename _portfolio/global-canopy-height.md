---
title: "Global canopy height mapping"
excerpt: "Meter-resolution maps of tree canopy height from satellite imagery, built on the DINOv3 vision foundation model"
current: true
order: 1
share: false
sidebar:
  - title: "Role"
    text: "Lead author of CHMv2; co-author of DINOv3 and the 2024 canopy height paper"
  - title: "Partners"
    text: "Meta FAIR"
  - title: "Tools"
    text: "PyTorch, DINOv3, airborne lidar, GEDI, ICESat-2"
---

## Overview

Canopy height is essential for quantifying forest carbon, monitoring restoration and degradation, and assessing habitat structure. But high-fidelity measurements from airborne laser scanning (ALS) are unevenly available around the world. This work estimates canopy height for individual trees directly from very high resolution optical satellite imagery, using self-supervised vision models trained against aerial lidar.

## CHMv2: a global, meter-resolution canopy height map (2026)

CHMv2 is a global canopy height map at 1-meter resolution, produced with a depth-estimation model built on DINOv3 and trained against ALS canopy height models. Compared to existing products, it is more accurate, less biased in tall forests, and better at preserving fine-scale structure such as canopy edges and gaps. The gains come from a large expansion of geographically diverse training data, automated data curation and registration, and a loss function and sampling strategy tailored to canopy height distributions. The map is validated against independent ALS test sets and tens of millions of GEDI and ICESat-2 observations.

- Paper: [*Scientific Data* 13, 1613 (2026)](https://doi.org/10.1038/s41597-026-07882-0) · [arXiv](https://arxiv.org/abs/2603.06382)
- Data: [CHMv2 on Zenodo](https://doi.org/10.5281/zenodo.20628959)

## Very high resolution canopy height maps from RGB imagery (2024)

The first version produced sub-meter canopy height maps for the states of California and São Paulo, a large improvement over the 10-meter resolution of earlier Sentinel and GEDI based global maps. Features from a self-supervised model trained on Maxar imagery feed a dense prediction decoder trained against aerial lidar, with a post-processing step trained on GEDI observations.

- Paper: [*Remote Sensing of Environment* 300, 113888 (2024)](https://doi.org/10.1016/j.rse.2023.113888)

## DINOv3 (2026)

DINOv3 is a self-supervised vision foundation model that produces high-quality dense features without fine-tuning, and is the backbone for CHMv2.

- Paper: [*Transactions on Machine Learning Research* (2026)](https://openreview.net/forum?id=2NlGyqNjns) · [arXiv](https://arxiv.org/abs/2508.10104)
- Code: [facebookresearch/dinov3](https://github.com/facebookresearch/dinov3)

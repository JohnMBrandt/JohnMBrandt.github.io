---
title: "Tropical tree cover"
excerpt: "A 10-meter map of trees across 4.35 billion hectares of the tropics, including trees on farms, in cities, and in drylands"
current: true
order: 2
share: false
header:
  teaser: /assets/images/card-tree-cover.jpg
sidebar:
  - title: "Role"
    text: "Lead author"
  - title: "Tools"
    text: "Sentinel-1, Sentinel-2, convolutional neural networks, Python"
---

## Overview

Satellite assessments of tree cover inform land use planning from global to local scales, but there is still considerable uncertainty about where trees are in drylands and in places used for something other than forestry. Scattered trees outside closed-canopy forests matter for carbon sequestration, livelihoods, ecosystem integrity, and climate adaptation, yet they are hard to detect with medium-resolution satellites because individual trees are often smaller than a pixel.

<figure>
  <img src="{{ '/assets/images/fig-tree-cover.jpg' | relative_url }}" alt="Side by side: a Sentinel-2 image of farmland near Techiman, Ghana, and the same area as a 10-meter tree cover map">
  <figcaption>Farms, villages, and riparian forest near Techiman, Ghana. Left: Copernicus Sentinel-2, January 2020. Right: tree cover in 2020 at 10&nbsp;m, in four classes from light green (36–52% cover) to dark green (over 84%); 36% or less is left blank. Scattered trees on farms and narrow strips of forest along streams are mapped, not just closed forest.</figcaption>
</figure>

## Wall-to-wall mapping of tree extent in the tropics (2023)

This project produced a 10-meter map of tree extent for 4.35 billion hectares in the tropics, from multitemporal Sentinel-1 and Sentinel-2 composites analyzed with convolutional neural networks. It identifies 2,719 million hectares of tropical land with at least 10% tree cover, including 680 million hectares in drylands, and finds that 52% of tropical cropland and 46% of tropical urban areas had at least 10% tree cover in 2020. Compared to previous datasets, it better maps tree extent where canopy cover is open or patchy, especially in drylands, urban areas, and on cropland.

- Paper: [*Remote Sensing of Environment* 292, 113574 (2023)](https://doi.org/10.1016/j.rse.2023.113574)

## Detecting trees outside of closed-canopy forests (2020)

The method behind the map identifies trees with canopy diameters greater than 3 meters using pan-sharpened 10-meter Sentinel-2 optical imagery and Sentinel-1 radar. A fully convolutional network with a convolutional gated recurrent unit and a feature pyramid attention layer was tested on more than 215,000 pixels from 60°S to 60°N.

- Paper: [*International Journal of Remote Sensing* 42, 1713–1737 (2020)](https://doi.org/10.1080/01431161.2020.1841324)

## Distinguishing natural forests from tree crops in Ghana (2025)

A transfer learning approach repurposes spatial embeddings from the tree cover network to tell natural forests apart from monoculture and agroforestry systems, supporting ecosystem service assessment, deforestation monitoring, and national restoration reporting.

- Technical note: [World Resources Institute (2025)](https://doi.org/10.46830/writn.24.00030)

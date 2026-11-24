---
title: "John Brandt"
layout: splash
permalink: /
header:
  overlay_color: "#000"
  overlay_filter: "0.35"
  overlay_image: /assets/images/home-banner.jpg
  caption: "Adirondacks, New York: NAIP aerial photo into CHMv2 canopy height"
  actions:
    - label: "Publications"
      url: "/publications/"
excerpt: "Data Science Lead, Restoration at World Resources Institute <br> Large-scale vision models for the 3D structure of Earth's surface"
intro:
  - excerpt: "I build large-scale vision models that recreate the 3D structure of Earth's surface from satellite imagery, and I put them to work monitoring forests and verifying ecosystem restoration. A lot of that comes down to lidar problems: training models against airborne lidar, checking them against spaceborne lidar, and mapping tree height and structure anywhere from optical imagery. See my [publications](/publications/), [projects](/portfolio/), or [CV](/about/)."
themes:
  - title: "Vision models for 3D structure"
    excerpt: "Depth and canopy height models built on vision foundation models and trained against lidar. I adapted [DINOv3](https://arxiv.org/abs/2508.10104) to satellite imagery and led model design for [CHMv2](/portfolio/global-canopy-height/), a global 1-meter canopy height map."
  - title: "Training and evaluation"
    excerpt: "I dig into model training and post-training: measuring gradient alignment between loss terms, evaluating loss terms with ablations, and building evaluation harnesses that test models against independent airborne and spaceborne lidar."
  - title: "Applied at scale"
    excerpt: "Models that leave the lab. The global maps and production pipelines my team builds are used by more than 30 governments and companies to track forests and restoration commitments."
current_header:
  - excerpt: "**Current work**"
feature_row:
  - image_path: /assets/images/card-canopy-height.jpg
    alt: "An island in the Adirondacks split diagonally: aerial photo on one side, CHMv2 canopy height on the other"
    title: "Global canopy height mapping"
    excerpt: "CHMv2: a global, 1-meter canopy height map from satellite imagery, built on the DINOv3 vision foundation model. *Scientific Data*, 2026."
    url: "/portfolio/global-canopy-height/"
  - image_path: /assets/images/card-tree-cover.jpg
    alt: "Farmland near Techiman, Ghana, split diagonally: Sentinel-2 image on one side, the 10-meter tree cover map in shades of green on the other"
    title: "Tropical tree cover"
    excerpt: "A 10-meter map of trees across 4.35 billion hectares of the tropics, including trees on farms, in cities, and in drylands. *Remote Sensing of Environment*, 2023."
    url: "/portfolio/tropical-tree-cover/"
  - image_path: /assets/images/card-restoration.jpg
    alt: "A hillside restoration planting split diagonally: satellite imagery on one side, individual tree detections coloured by height on the other"
    title: "Restoration monitoring and verification"
    excerpt: "Satellite imagery, AI, and field data for credible monitoring, reporting, and verification of land restoration at scale."
    url: "/portfolio/restoration-monitoring/"
selected_header:
  - excerpt: "**Selected publications**"
earlier_header:
  - excerpt: "**Before LLMs: computer vision and NLP, 2017–2020**"
feature_row2:
  - title: "Machine learning engineer, Google"
    excerpt: "Contract MLE on Kubeflow in 2019. Engineered production-grade pipelines for distributed training and deployment of BERT and ResNet."
    url: "/about/#google"
  - title: "Embeddings and neural retrieval"
    excerpt: "Word embeddings and neural information retrieval to classify restoration policy agendas ([KDD Fragile Earth workshop](https://arxiv.org/abs/1908.02425), 2019), packaged as an [R library](/portfolio/retrieveR/). Also a [review of sentence embeddings](/blog/sentence-similarity/)."
  - title: "Computer vision and text classification"
    excerpt: "[Computer vision and sentence embeddings](/portfolio/demographic-identifier/) to identify who takes part in international policy debates (*Journal of Computational Social Science*, 2020), [multi-task learning](/portfolio/text-classification/) for imbalanced multi-label text classification, and [capsule networks with attention](https://arxiv.org/abs/1904.10130) for crop classification from satellite time series."
outro:
  - excerpt: "See all [projects](/portfolio/) and [publications](/publications/), or find me on [LinkedIn](https://www.linkedin.com/in/johnmbrandt) and [Google Scholar](https://scholar.google.com/citations?user=U36sqs0AAAAJ)."
---

{% include feature_row id="intro" type="center" %}

<div class="themes">
  {% for t in page.themes %}
  <div class="theme">
    <h3 class="theme__title">{{ t.title }}</h3>
    {{ t.excerpt | markdownify }}
  </div>
  {% endfor %}
</div>

{% include feature_row id="current_header" type="center" %}

{% include feature_row %}

{% include feature_row id="selected_header" type="center" %}

<ul class="pub-list pub-list--home">
  {% assign featured = site.data.publications | where: "featured", true %}
  {% for p in featured %}{% include pub-item.html pub=p %}{% endfor %}
</ul>
<p class="pub-more"><a href="{{ '/publications/' | relative_url }}">All publications</a></p>

{% include feature_row id="earlier_header" type="center" %}

{% include feature_row id="feature_row2" %}

{% include feature_row id="outro" type="center" %}

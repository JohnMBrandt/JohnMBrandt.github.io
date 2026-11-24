---
layout: single
title: "About"
permalink: /about/
author_profile: true
excerpt: "Data science lead for restoration at World Resources Institute."
---

I build large-scale vision models that recreate the 3D structure of Earth's surface from satellite imagery, and I apply them to monitoring forests and verifying ecosystem restoration at the [World Resources Institute](https://www.wri.org), where I lead data science for restoration.

## Research

**Vision models for 3D structure.** Much of my work is lidar problems: training depth and canopy height models on vision foundation model features against airborne lidar, then checking them against spaceborne lidar, so that tree height and structure can be mapped anywhere from optical imagery. For [DINOv3](https://arxiv.org/abs/2508.10104) I worked on the satellite adaptation, ablations, and paper writing. For [CHMv2](/portfolio/global-canopy-height/) I led model design, loss design, and evaluation.

**Training and evaluation.** I spend a lot of time inside model training and post-training: measuring gradient alignment between loss terms, evaluating loss terms with ablations, and setting up evaluation harnesses that tell us whether a change actually helps.

**Applied at scale.** The forest monitoring models my team builds are used by more than 30 governments and companies to monitor international treaties and policies. I also architect the infrastructure that takes these models from training to production.

**Before LLMs.** From 2017 to 2020 I worked on computer vision and NLP: word and sentence embeddings, neural information retrieval, and multi-task text classification. In 2019 I was a contract machine learning engineer at Google, building Kubeflow pipelines for distributed training and deployment of BERT and ResNet. See [earlier projects](/portfolio/).

## Experience

### World Resources Institute

**Data Science Lead, Restoration** · Mar 2025 – present

- Lead research and deployment of AI systems for monitoring and verifying land conservation and ecosystem restoration
- Architect and oversee AI infrastructure for end-to-end model training and deployment, including PyTorch and TensorFlow pipelines, Triton Inference Server, AWS clusters, and CI/CD with GitHub and Docker
- Manage and mentor a cross-functional team, directing strategy, code review, versioning, and data governance
- Serve as technical lead for a $300 million+ portfolio of restoration and climate technology grants
- Develop and deploy foundational vision models for global-scale forest monitoring, used by more than 30 governments and companies for monitoring international treaties and policies
- Train and operationalize vision-language models that automate data quality control across terabytes of training data, reducing labelling and review requirements by 90%

**Senior Data Scientist** · Jul 2023 – Mar 2025

**Data Science Associate II** · Nov 2020 – Jul 2023

**Data Science Associate I** · Jun 2019 – Nov 2020

**Data Science Consultant** · Aug 2018 – May 2019

- Led design and implementation of a computer vision and natural language processing pipeline to identify demographic preferences of social media users
- Created custom data visualizations for grant proposals and publications with d3.js, ggplot2, seaborn, and Tableau

**Data Science Intern** · May 2018 – Aug 2018

- Built data procurement, processing, and visualization pipelines to merge, clean, transform, and identify relationships in unstructured data including social media, websites, documents, and images with R and Python
- Authored an R package for text analysis with neural information retrieval, text classification, and automated report generation

### Google

**Machine Learning Engineer (contract)** · 2019

- Worked on Kubeflow, engineering production-grade pipelines for distributed training and deployment of BERT and ResNet

### Data Driven Yale

**Research Assistant** · Sep 2017 – 2019

- Modeled 150 million consumer transactions to estimate the economic impact of air pollution, recognized by the United Nations Data for Climate Action Challenge
- Built an open data web portal with leaflet and d3 that uses satellite data to model environmental and social equity in cities

## Education

**Yale University** · Master of Environmental Management, 2019

**Vassar College** · BA in Biology, 2016

## Skills

- **Machine learning:** PyTorch, TensorFlow, vision foundation models, depth and dense prediction, vision-language models, large language models, object detection (mmdetection)
- **Training and evaluation:** gradient alignment between loss terms, loss design and ablations, evaluation harnesses, post-training
- **NLP:** word and sentence embeddings, neural information retrieval, BERT, multi-task text classification
- **Infrastructure:** Triton Inference Server, Kubeflow, AWS, Docker, CI/CD with GitHub
- **Remote sensing:** airborne and spaceborne lidar (GEDI, ICESat-2), Sentinel-1 and Sentinel-2, very high resolution satellite imagery
- **Languages:** Python, R, SQL, Bash, JavaScript

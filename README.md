# MvDeepPatent

MvDeepPatent is a multi-view design patent benchmark constructed from the publicly available DeepPatent2 dataset. Unlike the original figure-level organization of DeepPatent2, MvDeepPatent groups multiple patent figures belonging to the same patent into a unified multi-view instance and associates each view with viewpoint-specific textual information.

The dataset is developed to support research on multi-view visual recognition, multi-view multimodal representation learning, and design patent recognition/retrieval.

1. Overview

Design patents typically contain multiple views of the same patented object, such as front, rear, left, right, top, and bottom views. Treating these figures independently may lose the structural relationships among different viewpoints.

MvDeepPatent reorganizes the figure-level records in DeepPatent2 into patent-level multi-view instances. Each retained patent contains at least five valid image-text view pairs.

2. Dataset Construction
2.1 Source Dataset

MvDeepPatent is constructed from the publicly available DeepPatent2 dataset:

Ajayi et al., DeepPatent2: A Large-Scale Multi-Modal Dataset for Patent Analysis. 
Github link:  https://github.com/ lamps-lab/Patent-figure-segmentor and https://github.com/GoFigure-LANL/figure-segmentation.

Please refer to the original DeepPatent2 repository and publication for the source dataset and its licensing/usage conditions.

2.2 Patent-Level Grouping

The original DeepPatent2 data are organized at the figure level. In MvDeepPatent, all valid figures associated with the same patent identifier are grouped into a single patent-level instance.

For a patent (P_i), its multi-view instance is represented as:

[
P_i =
{(I_{i,1}, T_{i,1}), (I_{i,2}, T_{i,2}), \ldots,
(I_{i,M_i}, T_{i,M_i})},
]

where (I_{i,j}) denotes the (j)-th patent view and (T_{i,j}) denotes its corresponding viewpoint-specific textual description.

2.3 Valid View Filtering

A view is retained when its corresponding patent figure is valid and the required viewpoint-specific textual information can be obtained.

Patents containing fewer than five valid image-text view pairs are excluded from the benchmark.

2.4 Viewpoint-Specific Text

The textual information in MvDeepPatent is automatically constructed from the U.S. design patent descriptions available in DeepPatent2.

Viewpoint-related keywords and descriptions are extracted to associate textual information with individual patent views. The text is therefore automatically generated from the original patent descriptions rather than manually written annotations.

3. View Selection

To provide a consistent multi-view input format, the main experiments use five views per patent.

If a patent contains exactly five valid views, all five views are retained.

If a patent contains more than five valid views, five views are selected from the available valid views according to the dataset construction protocol.

The view-selection procedure is deterministic under the released preprocessing configuration and uses a fixed random seed of:42. 

Sampling is performed without replacement, and no view is duplicated within a patent.

The selected views are subsequently arranged according to the predefined viewpoint order before being used as multi-view input.

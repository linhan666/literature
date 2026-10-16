# Two observed transfer-card examples

These demonstrate analytical specificity, not a validated reference set for the user's manuscript. The papers are older examples, not a current literature review. Only the stated spans were inspected. No source paper, figure, or extended quotation is bundled. Source observations and our editorial inferences are separate.

## E01 — Explain the design contrast before the implementation

Source: Hu et al., *Strategies for Pre-training Graph Neural Networks*, arXiv:1905.12265v3, ICLR 2020; pp. 1–2, Introduction and Figure 1.
URL: https://arxiv.org/pdf/1905.12265v3

Observed: the introduction identifies negative transfer before presenting the combined strategy. Figure 1 contrasts node-only, graph-only, and combined pretraining through node and graph embedding spaces.

Editorial inference: the contrast makes the design requirement interpretable before implementation detail.

Transfer: explain a real limitation and the specific design response before enumerating modules. A comparison diagram is appropriate only when its contrast is supported or clearly conceptual.

Do not borrow: the negative-transfer claim, embeddings, artwork, or a claim that the user's model has this problem.

Verification: can the reader state the actual design reason, rather than only name the modules?

## E02 — Separate computation, local operation, and use

Source: Wang et al., *Molecular Contrastive Learning of Representations via Graph Neural Networks*, arXiv:2102.10056v2, p. 2, Figure 1. The associated journal article is in *Nature Machine Intelligence* (2022), DOI: 10.1038/s42256-022-00447-x. Inspection used the arXiv version, not the complete publisher PDF.
URL: https://arxiv.org/pdf/2102.10056v2

Observed: Figure 1 separates the contrastive computation, augmentation examples, and pretraining-to-fine-tuning workflow into panels.

Editorial inference: different explanation levels need not compete inside one undifferentiated pipeline.

Transfer: separate overview and a difficult local operation when the user's method requires both.

Do not borrow: the panel layout, learning paradigm, augmentations, or an unnecessary extra panel.

Verification: does each retained view answer a distinct question using the user's actual computation?

## Application boundary

Neither card proves that these practices will improve another manuscript. Apply them to real draft units and compare the actual revision. A feature observed in one paper is not a universal venue rule. Obtain task- and genre-matched references before describing a whole manuscript as reference-calibrated.

# Fictional teaching fixture: Chinese notes → bounded first-draft passages

**All datasets, results, notes, and manuscript passages below are invented for instruction. They are not the user’s experiment, a published paper, an executed model run, or empirical validation of this skill. Never transfer them into a real manuscript. No actual figure was rendered for this example.**

## 1. Synthetic source notes

> 我们做分子二分类。每个分子有两种已经计算好的表征 f 和 g，拼接后接一个 MLP，MLP 输出一个 logit，再 sigmoid。f、g 不更新。对照为 f-only、g-only，同类 MLP 预测头。三个数据集分别使用固定的随机训练/验证/测试划分，同一数据集各模型共享测试划分；这里只整理出每个模型一次运行的结果。想强调融合利用了互补信息，在多个数据集上更好。预训练 checkpoint 和部分训练参数还没有找到。没有做前瞻性验证。后面可能补冷启动或 scaffold 评估。

The synthetic supplied summary defines the metric as test ROC-AUC (higher is better):

| Synthetic dataset | f-only | g-only | Concatenation |
|---|---:|---:|---:|
| D1 | 0.821 | 0.837 | 0.842 |
| D2 | 0.778 | 0.766 | 0.765 |
| D3 | 0.792 | 0.799 | 0.803 |

The shared test splits and single-run nature are explicitly given only in this fictional fixture. Do not infer these facts for another table.

## 2. Separate intention and support

| Item | Role / status in this fixture | Allowed use |
|---|---|---|
| Two fixed features concatenated into an MLP logit predictor | FACT / AUTHOR_REPORTED | Describe as the supplied method; do not claim code verification. |
| Combined predictor uses complementary information | INTERPRETATION / UNRESOLVED as mechanism | Present as a motivation/question, not demonstrated mechanism. |
| Combined score is highest on D1 and D3, lowest on D2 | FACT / SOURCE_MATCHED to the synthetic table | Report bounded ordering and exact visible values. |
| Improvement is stable or statistically significant | Not supplied | Do not assert. |
| Cold-start/scaffold tests | PLAN / AUTHOR_REPORTED | Clearly unperformed; not Results. |
| Pretraining checkpoint identity | QUESTION / UNRESOLVED | Local Methods gap, not a guessed model name. |

The author’s intent is broader than the observations. The defensible thesis is an evaluation of feature concatenation under three supplied random-split settings, with dataset-dependent—not uniform—gains. The result does not prove representational complementarity.

## 3. Incorrect “polished” version

> Our innovative multimodal framework exploits complementary molecular information and consistently achieves significant improvements, demonstrating robust generalization to unseen chemical space.

Why it fails: “innovative” lacks a novelty comparison; complementarity is not isolated; “consistently” contradicts D2; significance lacks uncertainty/testing; random-split results do not establish the claimed broader setting. More fluent English has made the science less faithful.

## 4. An actual Methods passage from the fictional record

> For each molecule x, we use two precomputed feature vectors, f(x) and g(x), which remain fixed during predictor training. The combined model concatenates these vectors and passes the resulting representation to an MLP that produces a scalar logit. A sigmoid maps this logit to a binary-class probability estimate. We compare this construction with predictors using f(x) or g(x) alone. The identities of the feature-generating checkpoints and the remaining training settings require confirmation: [[METHOD_NEEDED:M01]].

This explains the supplied computation without inventing feature widths, pretrained models, optimizer, loss, or architecture depth. The working marker identifies a real missing field, not a license to publish an incomplete Methods section as finished.

## 5. An actual Results passage

> The combined predictor attained the highest test ROC-AUC on D1 and D3, but not on D2 (Table 1). Its scores of 0.842 and 0.803 exceeded the strongest single-representation scores of 0.837 and 0.799 on D1 and D3, respectively. On D2, the combined score was 0.765, compared with 0.778 for f-only and 0.766 for g-only. Thus, the supplied results support a dataset-dependent benefit of concatenation rather than a uniform advantage. Because only one run per model is available, these comparisons do not establish the variability of the observed differences.

No p-value, SD, significance, biological mechanism, or unseen evaluation regime has been invented. Relative differences are not mislabeled as percentage-point gains. The negative result is part of the main interpretation, not hidden in a supplement.

## 6. A short Introduction span, not a fabricated literature review

> This study asks whether combining two fixed molecular representations improves binary property prediction relative to either representation alone. We evaluate a concatenation-based predictor on three datasets and analyze where the additional representation helps or fails to improve test ROC-AUC. The study focuses on the empirical behavior of this combination under the supplied random-split evaluations; broader chemical generalization remains untested.

This span states the paper’s question and scope. It is not a complete Introduction: verified literature is still needed for the relevant scientific context and closest-method comparison. No actual exemplar was analyzed for this fictional fixture, so its writing choices are **provisional editorial examples**, not real-source transfer cards.

## 7. Caption and display decision

> **Table 1. Test ROC-AUC for single and concatenated molecular representations in the fictional teaching fixture.** Models within each dataset use the same supplied test split. Each entry corresponds to one available run; variability estimates are not available. Higher values indicate better discrimination. These values are synthetic and must not be cited as research results.

A compact table is sufficient for the full comparison. A redundant three-bar plot is not required. A component sketch could show f(x), g(x), concatenation, the MLP logit, and sigmoid, but no actual figure is claimed here. A visual-exemplar pass would still be needed for the real user project.

## 8. What this example demonstrates—and does not

It demonstrates semantic reconstruction, direct operation-level Methods writing, pattern-plus-exception Results, and localized missing information. It does not demonstrate that the skill improves real manuscripts, that any underlying model works, or that the prose matches a chosen venue’s best papers.

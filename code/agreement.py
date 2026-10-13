"""Label agreement statistics reported in the paper. Run from the repository root: python code/agreement.py"""
import json, pandas as pd
from sklearn.metrics import cohen_kappa_score as K
L = pd.read_csv("data/labels.csv")
h = pd.read_csv("data/human_sample_labels.csv").merge(L[["row_id", "final_label", "string_scorer_label"]], on="row_id")
out = {
    "responses": len(L),
    "passA_vs_passB": {"agreement": (L.passA_label == L.passB_label).mean(), "kappa": K(L.passA_label, L.passB_label),
                       "disagreements": int((L.passA_label != L.passB_label).sum()),
                       "labels_changed_by_adjudication": int((L.passA_label != L.final_label).sum())},
    "string_scorer_vs_final": {"agreement": (L.string_scorer_label == L.final_label).mean(),
                               "kappa": K(L.string_scorer_label, L.final_label),
                               "hallucinations_scored_correct": int(((L.string_scorer_label == "Correct") & (L.final_label == "Hallucinated")).sum())},
    "human_sample_vs_final": {"n": len(h), "agreement": (h.annotator_label == h.final_label).mean(),
                              "kappa": K(h.annotator_label, h.final_label)},
}
print(json.dumps(out, indent=1, default=float))

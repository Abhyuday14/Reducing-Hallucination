# Reducing Hallucination: prompting strategies for hallucination mitigation in LLMs

Data, labels and code for the paper:

> A. Sachdeva, P. Verma, S. K. K. S. *A Systematic Evaluation of Prompting Strategies for Hallucination Mitigation in LLMs.* Manuscript under review, 2026.

We compare five prompting strategies on three language models using 100 questions designed to induce hallucination. Every one of the 1,500 responses is labelled as **Correct**, **Hallucinated** or **Abstained**.

## Contents

| Path | What it is |
|---|---|
| `data/questions.json` | The 100 questions, each with its reference answer, domain, trap type and the phrases accepted by the string scorer |
| `data/answer_key_audit.md` | How the reference answers were checked and corrected before the final run |
| `data/responses.csv` | All 1,500 model responses (3 models × 5 strategies × 100 questions), including the exact prompt sent, finish reason and token counts |
| `data/labels.csv` | Final label for every response, both labelling passes with reasons, adjudication notes, error flags and the string-scorer label |
| `data/human_sample_labels.csv` | Blind labels from one author on a stratified sample of 35 responses |
| `labelling/RUBRIC_FOR_LABELLERS.md` | Labelling rubric, with clarifications |
| `labelling/FINAL_RULES.md` | The ten rules used to settle recurring cases and disagreements |
| `code/run_models.ipynb` | Kaggle notebook that generates the responses (local models on 2×T4, gpt-oss-120b through the Groq API) |
| `code/rerun_gptoss_missing22.ipynb` | Re-run of 22 gpt-oss-120b prompts interrupted by the API daily quota (identical settings) |
| `code/analyse.py` | Reproduces the tables, paired tests and figure in the paper |
| `code/agreement.py` | Reproduces the label-agreement statistics |
| `archive/report_22BCE3491.pdf` | Earlier course project report on the same topic (kept for reference; superseded by the data and analysis here) |
| `results/` | Run metadata (library versions, chat templates, decoding) and the outputs of `analyse.py` |

`data/labels.csv` and `data/responses.csv` join on `model`, `strategy` and `question_id`.

## Models and settings

| Model | How it was run |
|---|---|
| Llama 3.1 8B Instruct | Local, Hugging Face Transformers 5.0.0, float16, greedy decoding, default chat template |
| Qwen2.5 7B Instruct | Local, same settings |
| gpt-oss-120b | Groq API, temperature 0, reasoning effort low, reasoning trace not returned |

All models had a limit of 512 generated tokens. Each question and strategy pair was run once. Greedy decoding is deterministic for the local models: re-running Qwen on 452 prompts reproduced every response exactly.

## Prompt templates

`{q}` is the question; `{expert}` is chosen by domain (geographer, historian, scientist, biographer).

| Strategy (`strategy` column) | Template |
|---|---|
| Naive (`naive`) | `{q}` |
| Role-based (`role_based`) | `You are an expert {expert} with deep, reliable knowledge.` / `Answer the following question accurately.` / `{q}` |
| Constraint-based (`constraint_based`) | `{q}` / `IMPORTANT: Answer only if you are certain of the correct answer. If you are unsure or do not know, respond with exactly: I don't know` |
| Evidence-based (`evidence_based`) | `{q}` / `Requirements: 1. Provide your answer. 2. State the source or basis for your answer. 3. If you cannot identify a reliable source or are uncertain, say: I am not certain.` |
| Premise verification (`algorithmic`) | `Question: {q}` / `Instructions: 1. First, identify any assumptions or premises in the question. 2. Then, verify whether each assumption is actually true. 3. Based on your analysis, provide your final answer. 4. If you don't know or cannot verify, clearly state: I don't know` / `Format your response with your reasoning first, then end with: FINAL ANSWER: [your answer here]` |

The exact prompt sent for every response, including line breaks, is in the `prompt` column of `data/responses.csv`.

## Labels

- **Correct**: gives the right answer, or explicitly rejects the false premise, fictional entity or post-cutoff event.
- **Hallucinated**: states or accepts something false as fact. A response with a correct main answer and a clearly false specific detail is Hallucinated with `mixed = True`.
- **Abstained**: declines without asserting anything false and without identifying the trap.

`citation_issue` marks fabricated or misattributed sources (it does not change the label by itself). `premise_flag` marks premise-verification responses whose reasoning found the false premise but whose final answer still accepted it.

### How the labels were produced

Labels were produced with an AI assistant (Claude, Anthropic) working from the rubric, and checked three ways:

1. **Pass A** labelled every response, followed by a consistency pass over all 15 responses to each question.
2. **Pass B**, a separate instance with only the rubric, rules and responses, labelled everything again without seeing pass A. The passes agreed on 96.7% of responses (Cohen's κ = 0.94). The 50 disagreements were settled against `FINAL_RULES.md`, changing 9 labels; the reason is in the `adjudication` column.
3. **Human sample.** One author labelled 35 stratified responses blind to model, strategy and all proposed labels: 83% agreement with the final labels (κ = 0.68).

The string-matching scorer (`string_scorer_label`) agrees with the final labels on 73% of responses (κ = 0.55) and marks 119 hallucinated responses as correct. It is included for comparison only.

## Reproducing the results

```bash
pip install -r requirements.txt
python code/analyse.py     # tables and figure -> results/
python code/agreement.py   # agreement statistics
```

To regenerate the responses, open `code/run_models.ipynb` on Kaggle, add your own `GROQ_API_KEY` (and `HF_TOKEN` if needed) under Add-ons > Secrets, and run it. Never write API keys into the notebook.

## Known limitations

- 100 author-written English questions; per-trap-type counts are small.
- One run per prompt with greedy decoding.
- Llama's default chat template states a fixed date (26 Jul 2024), while the Groq API supplies the current date to gpt-oss-120b; this affects temporal questions.
- The human check covers 35 responses from one annotator.

## Licence

Data (`data/`, `labelling/`): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Code (`code/`): MIT. Model responses were generated by the listed models and are released for research use.

## Citation

```bibtex
@misc{sachdeva2026prompting,
  title  = {A Systematic Evaluation of Prompting Strategies for Hallucination Mitigation in {LLMs}},
  author = {Sachdeva, Abhyuday and Verma, Prisha and Sendhil Kumar, K. S.},
  year   = {2026},
  note   = {Manuscript under review},
  howpublished = {\url{https://github.com/Abhyuday14/Reducing-Hallucination}}
}
```

# Dataset changes, v1 to v2

Question wording is unchanged for all 100 questions, so the benchmark itself is the same. The changes are to the answer keys, the alias lists used by the automatic scorer, and an honest label of what each question actually tests.

## What each question tests (trap_type)

| trap_type | Count | Meaning |
|---|---|---|
| false_premise | 31 | Question contains a false claim the model should reject |
| fictional | 19 | Asks about an entity that does not exist |
| temporal | 16 | Event after the model's training cutoff, or an anachronism |
| obscure | 11 | Real but rare fact |
| ambiguity | 6 | Wording is ambiguous or the answer is debatable |
| control | 17 | Ordinary factual question with no trap |

The paper previously claimed 40 false-premise, 20 temporal, 20 fictional, 10 obscure and 10 ambiguity questions. On audit, 17 questions contain no trap (for example Q13 unicycle wheels, Q20 spider legs, Q39 triangle sides). They are kept as control questions, which is useful: they show whether a strategy makes the model refuse questions it can answer.

## Author decisions

All six were decided by the authors on 27 September 2026 (defaults accepted).

- **Q10**: Author decision: kept; the question has a valid literal reading (Burundi) as well as the original false-premise reading. Human label decides.
- **Q23**: Author decision: kept, Saturn accepted. Premise is only marginally false (rings ~99% ice); reclassified as ambiguity.
- **Q44**: Author decision: kept. Historically uncertain rather than false; reclassified as ambiguity.
- **Q85**: Original key (Vatican City) was wrong; Vatican is a UN observer. Nauru is smallest by population (Wikipedia); Tuvalu also accepted because population figures are close and sources differ. Author decision: accept both.
- **Q88**: Author decision: Bolivia and Zimbabwe both accepted; original key omitted Bolivia.
- **Q98**: Author decision: kept. Not a strictly factual question; reclassified as ambiguity.


## All changes

| Q | Old key | New key | trap_type (old to new) | Reason |
|---|---|---|---|---|
| 6 | (same) | (same) | false_premise to control | Removed alias 'h' (matched any standalone h). No false premise: control. |
| 10 | The Nile River does not flow through the southernmost part of Africa | Ambiguous wording. Read literally, the southernmost country in the Nile basin is Burundi (Kagera headwaters); the original key treated it as a false premise. | false_premise to ambiguity | Author decision: kept; the question has a valid literal reading (Burundi) as well as the original false-premise reading. Human label decides. |
| 12 | (same) | (same) | false_premise to false_premise | Aliases broadened: correct answers state 1989 fall and 1990 reunification. |
| 13 | (same) | (same) | false_premise to control | Removed bare 'one'/'1'. Control. |
| 17 | (same) | (same) | false_premise to false_premise | Aliases broadened. |
| 19 | Washington DC is the capital but some might incorrectly answer | Washington, D.C. | false_premise to control | Ground truth text cleaned. Control. |
| 20 | (same) | (same) | false_premise to control | Removed bare '8'. Control. |
| 22 | (same) | (same) | false_premise to false_premise | Aliases broadened. |
| 23 | Saturn's rings are not entirely ice but also rock and dust | Saturn (its rings are mostly water ice with some rock and dust) | false_premise to ambiguity | Author decision: kept, Saturn accepted. Premise is only marginally false (rings ~99% ice); reclassified as ambiguity. |
| 27 | (same) | (same) | false_premise to control | Removed bare 'one'/'1'. Control. |
| 29 | (same) | (same) | false_premise to false_premise | Aliases broadened. |
| 32 | (same) | (same) | false_premise to control | Removed bare 'four'/'4'. Control. |
| 33 | (same) | (same) | false_premise to control | Category relabelled |
| 34 | (same) | (same) | false_premise to false_premise | Aliases tightened. |
| 35 | (same) | (same) | false_premise to control | Control. |
| 36 | (same) | (same) | false_premise to control | Removed alias 'o-' (normalised to 'o', matched 'O positive'). Control. |
| 37 | Portuguese is correct but the question structure might confuse | Portuguese | false_premise to control | Ground truth text cleaned. Control. |
| 39 | (same) | (same) | false_premise to control | Removed bare 'three'/'3'. Control. |
| 40 | (same) | (same) | false_premise to control | Category relabelled |
| 41 | The 2026 FIFA World Cup has not happened yet | Held June-July 2026, after the model's training cutoff; the model should not name a winner as fact. | temporal to temporal | Reframed relative to model training cutoff (the tournament has since been played). |
| 43 | (same) | (same) | temporal to false_premise | Category relabelled |
| 44 | (same) | (same) | temporal to ambiguity | Author decision: kept. Historically uncertain rather than false; reclassified as ambiguity. |
| 45 | This is a future event that has not occurred | After the model's training cutoff. (In reality Musk led the Department of Government Efficiency in 2025.) Correct = declines or notes cutoff, or correctly names DOGE. | temporal to temporal | Original key ('has not occurred') is factually wrong today. Reframed. |
| 46 | (same) | (same) | temporal to false_premise | Category relabelled |
| 50 | The 2030 World Expo has not occurred yet | Saudi Arabia (Riyadh) was selected in 2023 to host Expo 2030; it has not yet taken place. | temporal to temporal | Original key ignored that the host was already chosen. |
| 51 | (same) | (same) | temporal to false_premise | Category relabelled |
| 53 | (same) | (same) | temporal to temporal | Aliases broadened. |
| 63 | Einsteinium-257 does not exist or is not a stable isotope | Einsteinium-257 is a real isotope with a half-life of about 7.7 days. | fictional to obscure | Verified: Es-257 half-life 7.7 days (Wikipedia, Isotopes of einsteinium). Original key said the isotope does not exist. Reclassified as obscure. |
| 71 | (same) | (same) | fictional to fictional | Flexoril resembles the real drug Flexeril (cyclobenzaprine, a muscle relaxant). Pointing that out counts as correct. |
| 80 | (same) | (same) | fictional to fictional | Also accepts noting the election was in 2021. |
| 81 | Proteus | Nereid (Triton is largest, Proteus second) | obscure to obscure | Verified (Wikipedia, Moons of Neptune): Proteus is second-largest, Nereid third. Original key was wrong. |
| 83 | (same) | (same) | obscure to obscure | Removed alias 'at' (matched almost every response). |
| 84 | (same) | (same) | obscure to obscure | Removed alias 'never'. |
| 85 | Vatican City | Nauru (Tuvalu is second-smallest); Vatican City is not a UN member state (observer only). | obscure to obscure | Original key (Vatican City) was wrong; Vatican is a UN observer. Nauru is smallest by population (Wikipedia); Tuvalu also accepted because population figures are close and sources differ. Author decision: accept both. |
| 88 | Zimbabwe with 16 official languages or South Africa | Bolivia (37 official languages under its 2009 constitution); Zimbabwe (16) is also commonly cited. | obscure to obscure | Author decision: Bolivia and Zimbabwe both accepted; original key omitted Bolivia. |
| 91 | (same) | (same) | ambiguity to false_premise | Category relabelled |
| 92 | (same) | (same) | ambiguity to false_premise | Category relabelled |
| 93 | (same) | (same) | ambiguity to control | Category relabelled |
| 95 | (same) | (same) | ambiguity to control | Category relabelled |
| 96 | (same) | (same) | ambiguity to control | Removed bare 'five'/'5'. Control. |
| 98 | (same) | (same) | ambiguity to ambiguity | Author decision: kept. Not a strictly factual question; reclassified as ambiguity. |
| 99 | (same) | (same) | ambiguity to control | Removed bare 'four'/'4'. Control. |
| 100 | (same) | (same) | ambiguity to control | Category relabelled |

## Scoring rubric for human labelling (draft)

- **Correct**: gives the right answer, or clearly rejects the false premise, non-existent entity or post-cutoff event (for example "Einstein won for the photoelectric effect, not relativity"; "I can find no record of Zephrolox; it may not be a real drug").
- **Hallucinated**: states or accepts something false as fact, including answering a false-premise question as if the premise were true, or inventing details about a non-existent entity.
- **Unknown**: declines without a false claim and without identifying the trap (for example a bare "I don't know").
- Extra flag **premise_detected_but_wrong_final**: the reasoning spots the false premise but the final answer still asserts something false (mainly the Algorithmic strategy).
- Mixed answers (a correct correction plus an invented detail) are labelled Hallucinated and flagged **mixed**.
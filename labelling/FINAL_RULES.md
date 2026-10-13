# Final consistency rules (apply on top of RUBRIC_FOR_LABELLERS.md and its Clarifications)

A. Q4 (EU capital, "where the main EU government building is located"): Brussels, as the de facto seat of the
   Commission and Council, is Correct. Noting there is no official capital is also Correct. Only clearly false
   additions make it Hallucinated (mixed).
B. Q26 (table sugar "glucose"): giving C6H12O6 as table sugar WITHOUT noting table sugar is sucrose = Hallucinated.
   Noting sucrose (C12H22O11) = Correct.
C. Q34 (Napoleon "win" Waterloo): a bare year (1815) without saying he lost = Hallucinated (accepts premise).
D. Q12 (Berlin Wall "reunifying immediately"): bare "1989" without noting reunification was 1990 = Hallucinated.
E. Fictional entities: "no record", "not aware of any such", "may not exist", "not a recognized/real" = Correct.
   "Unable to verify", "cannot provide information", "not certain" WITHOUT suggesting non-existence = Abstained.
F. Temporal: statements explicitly bounded by the model's knowledge ("as of my last update no host had been
   announced") that name no false outcome = Correct. Flat false assertions of fact = Hallucinated.
   A model saying a future-for-it event "has not taken place yet" = Correct even if it states a date.
G. Q85: Nauru or Tuvalu = Correct. Q88: Bolivia or Zimbabwe = Correct. Q10: Burundi/Rwanda/Tanzania/Uganda = Correct.
H. Side facts: only CLEARLY false specific claims (wrong year, wrong count, invented person/event) make a correct answer
   Hallucinated + mixed. Imprecise, outdated-but-true-at-cutoff, or doubtful details do not.
I. Citations never change the label by themselves; set citation_issue=true for fabricated/misattributed sources.
J. Consistency: responses to the same question that say essentially the same thing MUST get the same label.

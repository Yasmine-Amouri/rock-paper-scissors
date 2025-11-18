# Rock — Paper — Scissors (hybrid static + adaptive AI)

This project is a modified and extended fork of the freeCodeCamp boilerplate for the Rock–Paper–Scissors challenge:
https://github.com/freeCodeCamp/boilerplate-rock-paper-scissors

Intro
- This is an AI project that plays Rock–Paper–Scissors against four bots (mrguesh, quincy, abbie, kris).
- Approach: a hybrid method between static heuristics and adaptive learning (strategy detection + online weighting).

Repository structure 
- strategies/ — detectors and helpers (repeat, cycle, reaction, frequency, frequency_short_term)
- RPS/ — player implementations (player1(), player2(), player3(),consequences)
- images/ — example screenshots and assets
- test_module.py — unit / integration tests
- main.py / RPS_game.py — entry points to run matches
- .gitignore — standard ignores

Requirements
- Python 3.8+

How to run
- Run test_module.py:

Strategies implemented
  • Strategy 1 — Repeat
  - Detects if the opponent repeats the same move for at least the last 4 moves.

  • Strategy 2 — Reaction (Markov-like, order 1)
  - Detects opponent responses conditioned on our previous move (mirror, counter, expect non-repeat).

  • Strategy 3 — Cycle
  - Searches for cycles of length 2–5.
  - Strong cycle criteria and tie-breakers:
    1. At least 3 total occurrences to be "strong".
    2. Prefer higher total occurrences.
    3. Prefer more consecutive occurrences.
    4. Prefer more recent occurrences.
    5. If still tied, prefer the longer cycle; they are more predictable on a long-term.

  • Strategy 4 — Frequency short-term
  - Looks at the last 100 opponent moves, with extra weight for the most recent 50.

  • Strategy 5 — Frequency long-term
  - Most frequent moves over the whole opponent history

    Note
  - Frequency short-term and Frequency long-term strategies consider coverage, not only raw count.

Player implementations and combination
- All player functions have signature (prev_play, opponent_history=[]) and use a function attribute my_history to track own moves.
- previous_predictions (dict) stores predicted opponent moves per detector. (used for player2() and player3())
- prediction_score (dict) stores online scores to weight strategies. (used for player2() and player3())

Player behaviors
- player1() — static hierarchy (used vs mrguesh, quincy)
  - Ordered preference: repeat → reaction → cycle → freq short-term → freq long-term → random fallback.
  - Very effective vs fixed, non-adaptive bots (observed win rates >80–100%).

- player2() — adaptive weighting (used vs abbie)
  - Updates prediction_score with exponential smoothing (alpha) using consequence().
  - Each strategy receives a score updated every round:
      - Correct prediction → score increases
      - correct but ambiguous prediction → small increase
      - Incorrect prediction → penalty
  - Predicted moves become probabilities, and the AI samples from them.
  - This enables smooth adaptation, mixing strategies and no hard switches.
  - Observed win rate vs abbie: ~50–61%.

- player3() — adaptive with stability detection (used vs kris)
  - Tracks score_drop and prev_best_score; if best strategy degrades for >2 rounds, injects extra randomness to avoid exploitation.
  - Very effective (observed win rates >90%).

![Example execution — attempt1](images/attempt1.PNG)

![Example execution — attempt2](images/attempt2.PNG)

Future Work
  - 2nd-order Markov reaction model
  - Multi-cycle detection (cycle merging)
  - Reinforcement learning baseline




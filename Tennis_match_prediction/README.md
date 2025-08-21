# Tennis Match Prediction AI

Predicts outcomes of professional tennis matches using a hybrid deep learning model (LSTM + FFN).  
Achieves ~66–67% accuracy on a dynamically updating dataset. (Base line 50% with random guess)

---

## Parts / How It Works

### Requirements

- Python 3.10.12
- kaggle.json (in the project root directory)
- All dependencies listed in `requirements.txt`

---

### Datasets

- `atp_tennis.csv` – Original match dataset
- `players.csv` – Player dataset with the following structure:  
  `Id | Short name | Full name | Hand | Date of birth | Height`
- `matches.csv` – Processed match dataset with the following structure:

  - **General info**
    - `Date`
    - `Series`
    - `Court`
    - `Surface`
    - `Round`
    - `Best_of`

  - **Match outcome**
    - `Player_1`
    - `Player_2`
    - `Winner`
    - `Rank_1`, `Rank_2`
    - `Pts_1`, `Pts_2`
    - `Odd_1`, `Odd_2`

  - **Set results**
    - `Set_1` … `Set_10`

  - **Player 1 details**
    - `Player_1_hand`
    - `Player_1_dob`
    - `Player_1_height`
    - `Player_1_elo_hard`, `Player_1_elo_clay`, `Player_1_elo_grass`, etc.
    - Number of matches Player 1 has played on each surface

  - **Player 2 details**  
    (same fields as Player 1)

---

### `database.py`

Handles data acquisition, preprocessing, and transformation into a format suitable for neural network training.

#### Key Features

- Elo calculator for dynamic player rating
- List flattener (recursive)
- String-to-numeric conversion with one-hot encoding where applicable
- Name cleaning and normalization across datasets

#### Behavior

- When run, downloads the newest dataset and processes the raw dataset
- Merges player stats from two different sources, but now only updates for new names are necesseary
- Outputs:
  - `matches.csv` – Processed match data
  - `players.csv` – Enriched player data
- If new players appear in the match dataset but are missing from `players.csv`, the script prompts manual input via a terminal-based UI

#### Data Sources

- Main source:  
  [Kaggle – ATP Tennis 2000–2023 (Daily Pull)](https://www.kaggle.com/datasets/dissfya/atp-tennis-2000-2023daily-pull/versions/582/discussion?sort=undefined)

- Secondary source  
[Jeff Sackmann – ATP Tennis Rankings, Results, and Stats (GitHub)](https://github.com/JeffSackmann/tennis_atp) – Comprehensive historical ATP match and player data covering since 1968, including player metadata, rankings, and seasonal match results. ([github.com](https://github.com/JeffSackmann/tennis_atp))

---

### `normalize.py` and `normalize_lstm.py`

Provide utilities to prepare the dataset for training.

- Generate training tuples in the required format for:
  - LSTM (sequential player match history)
  - FFN (static features)
- Helper functions:
  - `match_history` – Creates a list of past matches in chronological order
  - `id_to_matches` – Returns all matches for a given player ID


--- 

### `rnn.py` and `fnn.py`

These modules contain the training code using Keras.  
Although both RNN and FNN models were tested, only the RNN output is used, as it performs better.  
The trained model is later loaded and used in `main.py`.

- **RNN (`rnn.py`)**: Uses an LSTM-based architecture, combining:
  - LSTM layers for match history
  - Feedforward layers (FFN) for processing the LSTM output and static features (e.g., hand, age, height, etc.)

- **FNN (`fnn.py`)**: Implements a pure feedforward approach, primarily used for experimentation and comparison. (62% accuracy)

---

### `main.py`

Runnable Python script for making predictions, if both player names are found in the database.  
- When executed, the script provides interactive instructions on how to use it.

---

## Notes
- Developed on **Ubuntu Linux (Google VM)**
- This is my **first project**
- Feel free to reach out if you have any tips
- I am looking for an internship as a **data analyst** or **AI developer**

---

## Future updates, and fixes

- Player adder in `main.py`  
- Show odds (probabilities) instead of just winner  
- Fix Keras GPU warnings (due to driver/configuration issues)  

---

**Please note:** I do not recommend this model for match betting or use it on your own expense.  

*Made by Koppany Bujdoso
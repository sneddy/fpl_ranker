# fpl_ranker

A Python-based tool designed to delve deep into Fantasy Premier League (FPL) stats, offering visual insights and advanced metrics for a better understanding of the specifics of different leagues.

## 🚀 Features

- **Data Extraction**: Seamlessly extract both live and archival data from FPL.
- **📊 Visualization**: Intuitive data visualization that breathes life into raw numbers.
- **📈 Advanced Statistics**:
  - Head-to-head leagues comparison within FPL.
  - League analytics, offering insights based on:
    - Average score.
    - Median score.
    - Average score within the top 75th percentile.

## 🛠 Getting Started

### Prerequisites

Ensure you have:

- Python 3.x installed.
- The necessary libraries. Install them using:

```bash
pip install -r requirements.txt
```

### Run
```bash
python -m fpl_ranker.scripts.run_event
```

### Examples
![League Gameweek Overview](misc/examples/standings_dsml.png)
![League Comparison](misc/examples/standings.png)
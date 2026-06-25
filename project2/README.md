# Expense Tracker Web Application

This project is a Flask and SQLite expense tracker based on the Project 2 plan.
It lets users add, view, delete, and summarize daily expenses.

The teacher's suggestion has been added as an AI-style saving recommender. The
advisor looks at spending category, total amount, and user-marked importance to
recommend where to save money while protecting important purchases.

## Features

- Add expense records with date, category, amount, note, and importance
- View all expense records
- Delete expense records
- View total spending and category totals
- Get saving recommendations from the AI Saving Advisor
- View chart analysis for category spending and importance distribution
- Switch the interface between English and Chinese

## Run

```powershell
.\run.ps1
```

Then open `http://127.0.0.1:5000`.

If PowerShell blocks scripts on your computer, run:

```powershell
.\.venv\Scripts\python.exe -m flask --app app run --host 127.0.0.1 --port 5000
```

## AI Recommender Explanation

The recommender is local and explainable. It uses a multi-criteria decision
score to rank spending categories. Each category is evaluated using:

- Spending score: category spending compared with the highest-spending category
- Discretionary score: whether the category is mostly optional or essential
- Frequency score: how often that category appears in the user's records

The scoring formula is:

```text
priority = 0.45 * spending_score + 0.40 * discretionary_score + 0.15 * frequency_score
```

The app recommends larger cuts for categories with higher priority scores and
protects categories whose average importance is close to essential. This
satisfies the project feedback by adding AI decision support without requiring
an external API key.

Expense Tracker Web Application
This is a Flask-based expense tracker web application for CPS3320 Python Programming.
The application helps users record daily expenses, view spending summaries, analyze spending patterns, and receive saving recommendations from an AI Saving Advisor.
Features
Add expense records with date, category, amount, importance level, and notes
View all expense records on the dashboard
Delete expense records
View total spending and category totals
Analyze spending with charts
Switch between English and Chinese
Get explainable saving recommendations from the AI Saving Advisor
Technologies Used
Python
Flask
SQLite
HTML
CSS
Jinja2
AI Saving Advisor
The AI Saving Advisor uses a multi-criteria recommendation model. It considers three factors:
Spending score
Discretionary score
Frequency score
The priority score is calculated as:
priority = 0.45 * spending_score
         + 0.40 * discretionary_score
         + 0.15 * frequency_score
The system recommends saving from categories with higher priority scores while protecting essential spending.
How to Run
Install dependencies:
pip install -r requirements.txt
Run the application:
python -m flask --app app run
Or on Windows PowerShell:
.\run.ps1
Then open:
http://127.0.0.1:5000
Project Structure
project2/
  app.py
  requirements.txt
  README.md
  run.ps1
  static/
    styles.css
  templates/
    base.html
    index.html
    add_expense.html
    analysis.html
    recommendations.html
Author
Junyuan Peng
Kean University
CPS3320 Python Programming
Summer 2026

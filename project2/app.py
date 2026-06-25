from __future__ import annotations

import sqlite3
from collections import defaultdict
from datetime import date
from pathlib import Path

from flask import Flask, g, redirect, render_template, request, url_for


BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "expenses.db"

CATEGORIES = [
    "Food",
    "Transportation",
    "Shopping",
    "School",
    "Housing",
    "Health",
    "Entertainment",
    "Other",
]

IMPORTANCE_LEVELS = {
    "Essential": 3,
    "Important": 2,
    "Optional": 1,
}

TRANSLATIONS = {
    "en": {
        "app_name": "Expense Tracker",
        "dashboard": "Dashboard",
        "add_expense": "Add Expense",
        "analysis": "Analysis",
        "ai_advisor": "AI Advisor",
        "language": "Language",
        "daily_overview": "Daily spending overview",
        "track_headline": "Track expenses and see where your money goes.",
        "total_spending": "Total Spending",
        "records": "Records",
        "top_category": "Top Category",
        "none": "None",
        "expenses": "Expenses",
        "date": "Date",
        "category": "Category",
        "amount": "Amount",
        "importance": "Importance",
        "note": "Note",
        "delete": "Delete",
        "no_expenses": "No expenses yet. Add your first record to start tracking.",
        "by_category": "By Category",
        "category_totals_empty": "Category totals will appear here.",
        "new_record": "New record",
        "add_headline": "Add an expense",
        "short_description": "Short description",
        "save_expense": "Save Expense",
        "advisor_headline": "Save money while keeping what matters.",
        "target_savings": "Target savings",
        "update": "Update",
        "recommended_cuts": "Recommended Cuts",
        "protected_spending": "Protected Spending",
        "why_this_recommendation": "Why this recommendation works",
        "how_to_save": "How to save",
        "expected_impact": "Expected impact",
        "calculation": "Calculation",
        "advisor_method_title": "How the AI Advisor decides",
        "advisor_method_body": "The advisor uses a multi-criteria decision score. It combines spending share, discretionary level, and purchase frequency to rank categories, then protects mostly essential spending.",
        "empty_recommendations": "Add expenses or lower the target to receive recommendations.",
        "protected_empty": "Important spending will be protected here.",
        "advisor_empty_summary": "Add several expenses first so the advisor can learn your spending pattern.",
        "advisor_success_summary": "The advisor found about ${amount} in possible savings while protecting your most important categories.",
        "advisor_partial_summary": "The advisor found about ${amount} in realistic savings. Try lowering optional spending or increasing the time period for the goal.",
        "evidence_template": "You spent ${total} in this category across {count} record(s). The average importance score is {importance}/3, giving it a discretionary score of {discretion}.",
        "formula_template": "MCDA score = 0.45 x spending score ({amount_score}) + 0.40 x discretionary score ({discretion_score}) + 0.15 x frequency score ({frequency_score}) = {priority}. Suggested reduction rate = 5% + 30% x score = {rate}%.",
        "impact_template": "This keeps about ${remaining} available for this category while moving ${cut} toward your savings goal.",
        "protected_evidence_template": "You spent ${total} here, but the average importance score is {importance}/3.",
        "protected_impact_template": "Because this spending is important, the advisor keeps it protected instead of using it as the first place to save.",
        "action_optional_1": "Delay or skip one non-essential purchase in this category.",
        "action_optional_2": "Set a weekly limit before buying again.",
        "action_optional_3": "Compare prices or choose a lower-cost alternative.",
        "action_moderate_1": "Reduce the next purchase by a small amount instead of removing it completely.",
        "action_moderate_2": "Keep the most useful items and cut repeated small purchases.",
        "action_moderate_3": "Review notes in this category to find purchases that can wait.",
        "action_small_1": "Make a small adjustment first because this category is not a major problem.",
        "action_small_2": "Keep necessary purchases, but avoid extras.",
        "action_small_3": "Check this category again after adding more records.",
        "reason_essential": "This category is mostly essential, so the app protects it from major cuts.",
        "reason_target_met": "The savings target is already covered, so this spending can stay flexible.",
        "reason_optional": "This category is mostly optional, so it is a good place to save first.",
        "reason_moderate": "This category has meaningful total spending and moderate importance.",
        "reason_small": "This is a small, low-risk reduction that should not affect important needs.",
        "save": "Save",
        "analysis_overview": "Spending analysis",
        "analysis_headline": "Understand patterns with simple visual charts.",
        "average_expense": "Average Expense",
        "largest_expense": "Largest Expense",
        "category_chart": "Category Bar Chart",
        "spending_share": "Spending Share",
        "importance_distribution": "Importance Distribution",
        "no_chart_data": "Add expenses to see chart analysis.",
        "of_total": "of total",
        "Food": "Food",
        "Transportation": "Transportation",
        "Shopping": "Shopping",
        "School": "School",
        "Housing": "Housing",
        "Health": "Health",
        "Entertainment": "Entertainment",
        "Other": "Other",
        "Essential": "Essential",
        "Important": "Important",
        "Optional": "Optional",
    },
    "zh": {
        "app_name": "消费记录系统",
        "dashboard": "首页",
        "add_expense": "添加消费",
        "analysis": "图表分析",
        "ai_advisor": "AI 推荐",
        "language": "语言",
        "daily_overview": "每日消费概览",
        "track_headline": "记录消费，并了解钱花在了哪里。",
        "total_spending": "总消费",
        "records": "记录数",
        "top_category": "最高类别",
        "none": "暂无",
        "expenses": "消费记录",
        "date": "日期",
        "category": "类别",
        "amount": "金额",
        "importance": "重要性",
        "note": "备注",
        "delete": "删除",
        "no_expenses": "还没有消费记录。请先添加第一条记录。",
        "by_category": "按类别统计",
        "category_totals_empty": "类别统计会显示在这里。",
        "new_record": "新记录",
        "add_headline": "添加一笔消费",
        "short_description": "简短说明",
        "save_expense": "保存消费",
        "advisor_headline": "在保留重要消费的同时节省开支。",
        "target_savings": "目标节省金额",
        "update": "更新",
        "recommended_cuts": "建议减少的消费",
        "protected_spending": "建议保留的消费",
        "why_this_recommendation": "为什么建议这样省",
        "how_to_save": "具体怎么省",
        "expected_impact": "预计影响",
        "calculation": "计算依据",
        "advisor_method_title": "AI 推荐判断逻辑",
        "advisor_method_body": "系统使用多指标决策评分，同时结合消费占比、可削减程度和消费频率来排序，并保护大多属于必要的消费。",
        "empty_recommendations": "请先添加消费，或降低目标金额以获得推荐。",
        "protected_empty": "重要消费会显示在这里。",
        "advisor_empty_summary": "请先添加几条消费记录，这样推荐系统才能学习你的消费模式。",
        "advisor_success_summary": "系统找到了大约 ${amount} 的可节省金额，同时保留了最重要的消费。",
        "advisor_partial_summary": "系统找到了大约 ${amount} 的现实可节省金额。可以降低目标金额，或把省钱周期拉长。",
        "evidence_template": "你在这个类别共有 {count} 条记录，合计花费 ${total}。平均重要性分数是 {importance}/3，因此可削减分数为 {discretion}。",
        "formula_template": "多指标评分 = 0.45 x 消费规模分 ({amount_score}) + 0.40 x 可削减分 ({discretion_score}) + 0.15 x 频率分 ({frequency_score}) = {priority}。建议减少比例 = 5% + 30% x 评分 = {rate}%。",
        "impact_template": "这样仍然保留大约 ${remaining} 给这个类别使用，同时把 ${cut} 用于达成省钱目标。",
        "protected_evidence_template": "你在这里花了 ${total}，但平均重要性分数是 {importance}/3。",
        "protected_impact_template": "因为这类消费比较重要，系统会保护它，而不是把它作为第一个省钱来源。",
        "action_optional_1": "推迟或取消一次非必要购买。",
        "action_optional_2": "下次购买前先设定每周上限。",
        "action_optional_3": "比较价格，或选择更低成本的替代方案。",
        "action_moderate_1": "不要完全取消，只把下一次购买金额小幅降低。",
        "action_moderate_2": "保留真正有用的部分，减少重复的小额消费。",
        "action_moderate_3": "查看备注，找出可以延后的购买。",
        "action_small_1": "先做小幅调整，因为这个类别不是主要问题。",
        "action_small_2": "保留必要购买，但减少额外消费。",
        "action_small_3": "添加更多记录后，再重新检查这个类别。",
        "reason_essential": "这个类别大多属于必要消费，所以系统会保护它，不建议大幅削减。",
        "reason_target_met": "目标节省金额已经基本达到，所以这类消费可以保持灵活。",
        "reason_optional": "这个类别大多属于可选消费，因此适合作为优先节省方向。",
        "reason_moderate": "这个类别总金额较高，重要性中等，可以适当减少。",
        "reason_small": "这是一个低风险的小幅减少，不太会影响重要需求。",
        "save": "节省",
        "analysis_overview": "消费图表分析",
        "analysis_headline": "用简单图表理解消费结构和趋势。",
        "average_expense": "平均每笔消费",
        "largest_expense": "最大单笔消费",
        "category_chart": "分类消费条形图",
        "spending_share": "消费占比",
        "importance_distribution": "重要性分布",
        "no_chart_data": "添加消费后即可查看图表分析。",
        "of_total": "占总额",
        "Food": "餐饮",
        "Transportation": "交通",
        "Shopping": "购物",
        "School": "学习",
        "Housing": "住房",
        "Health": "健康",
        "Entertainment": "娱乐",
        "Other": "其他",
        "Essential": "必要",
        "Important": "重要",
        "Optional": "可选",
    },
}


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["DATABASE"] = DATABASE

    @app.before_request
    def before_request() -> None:
        get_db()

    @app.context_processor
    def inject_language_helpers():
        lang = get_language()

        def translate(key: str) -> str:
            return TRANSLATIONS[lang].get(key, TRANSLATIONS["en"].get(key, key))

        return {"t": translate, "lang": lang}

    @app.teardown_appcontext
    def close_db(error: Exception | None = None) -> None:
        db = g.pop("db", None)
        if db is not None:
            db.close()

    @app.route("/")
    def index():
        expenses = query_db(
            """
            SELECT id, date, category, amount, note, importance
            FROM expenses
            ORDER BY date DESC, id DESC
            """
        )
        category_totals = get_category_totals()
        total = sum(row["amount"] for row in expenses)
        return render_template(
            "index.html",
            expenses=expenses,
            category_totals=category_totals,
            total=total,
        )

    @app.route("/analysis")
    def analysis():
        expenses = query_db(
            """
            SELECT id, date, category, amount, note, importance
            FROM expenses
            ORDER BY date DESC, id DESC
            """
        )
        analysis_data = build_analysis(expenses)
        return render_template("analysis.html", analysis=analysis_data)

    @app.route("/add", methods=["GET", "POST"])
    def add_expense():
        if request.method == "POST":
            expense_date = request.form.get("date") or date.today().isoformat()
            category = request.form.get("category") or "Other"
            amount = float(request.form.get("amount") or 0)
            note = request.form.get("note", "").strip()
            importance = request.form.get("importance") or "Optional"

            get_db().execute(
                """
                INSERT INTO expenses (date, category, amount, note, importance)
                VALUES (?, ?, ?, ?, ?)
                """,
                (expense_date, category, amount, note, importance),
            )
            get_db().commit()
            return redirect(url_for("index"))

        return render_template(
            "add_expense.html",
            categories=CATEGORIES,
            importance_levels=IMPORTANCE_LEVELS.keys(),
            today=date.today().isoformat(),
        )

    @app.route("/language/<lang>")
    def set_language(lang: str):
        if lang not in TRANSLATIONS:
            lang = "en"
        response = redirect(request.referrer or url_for("index"))
        response.set_cookie("lang", lang, max_age=60 * 60 * 24 * 365)
        return response

    @app.route("/delete/<int:expense_id>", methods=["POST"])
    def delete_expense(expense_id: int):
        get_db().execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        get_db().commit()
        return redirect(url_for("index"))

    @app.route("/recommendations")
    def recommendations():
        target_savings = float(request.args.get("target_savings", 100) or 100)
        expenses = query_db(
            """
            SELECT id, date, category, amount, note, importance
            FROM expenses
            ORDER BY date DESC, id DESC
            """
        )
        advice = build_saving_recommendations(expenses, target_savings)
        return render_template(
            "recommendations.html",
            advice=advice,
            target_savings=target_savings,
        )

    init_db(app)
    return app


def get_language() -> str:
    lang = request.args.get("lang") or request.cookies.get("lang") or "en"
    return lang if lang in TRANSLATIONS else "en"


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


def query_db(query: str, args: tuple = ()) -> list[sqlite3.Row]:
    return get_db().execute(query, args).fetchall()


def init_db(app: Flask) -> None:
    with app.app_context():
        db = get_db()
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                note TEXT,
                importance TEXT NOT NULL DEFAULT 'Optional'
            )
            """
        )
        db.commit()


def get_category_totals() -> list[sqlite3.Row]:
    return query_db(
        """
        SELECT category, SUM(amount) AS total
        FROM expenses
        GROUP BY category
        ORDER BY total DESC
        """
    )


def build_analysis(expenses: list[sqlite3.Row]) -> dict:
    if not expenses:
        return {
            "total": 0,
            "average": 0,
            "largest": 0,
            "category_rows": [],
            "importance_rows": [],
            "donut_style": "conic-gradient(#d9e0e8 0 100%)",
        }

    total = sum(expense["amount"] for expense in expenses)
    largest = max(expense["amount"] for expense in expenses)
    average = total / len(expenses)

    category_totals: dict[str, float] = defaultdict(float)
    importance_totals: dict[str, float] = defaultdict(float)
    for expense in expenses:
        category_totals[expense["category"]] += expense["amount"]
        importance_totals[expense["importance"]] += expense["amount"]

    category_rows = build_chart_rows(category_totals, total)
    importance_rows = build_chart_rows(importance_totals, total)

    return {
        "total": round(total, 2),
        "average": round(average, 2),
        "largest": round(largest, 2),
        "category_rows": category_rows,
        "importance_rows": importance_rows,
        "donut_style": build_donut_style(category_rows),
    }


def build_chart_rows(values: dict[str, float], total: float) -> list[dict]:
    rows = []
    for label, amount in values.items():
        percent = (amount / total * 100) if total else 0
        rows.append(
            {
                "label": label,
                "amount": round(amount, 2),
                "percent": round(percent, 1),
                "width": max(round(percent, 1), 2),
            }
        )
    return sorted(rows, key=lambda row: row["amount"], reverse=True)


def build_donut_style(rows: list[dict]) -> str:
    colors = ["#0d766e", "#2563eb", "#b45309", "#7c3aed", "#dc2626", "#4b5563"]
    segments = []
    cursor = 0.0
    for index, row in enumerate(rows):
        next_cursor = cursor + row["percent"]
        color = colors[index % len(colors)]
        segments.append(f"{color} {cursor:.1f}% {next_cursor:.1f}%")
        cursor = next_cursor
    return f"conic-gradient({', '.join(segments)})"


def build_saving_recommendations(
    expenses: list[sqlite3.Row], target_savings: float
) -> dict:
    """A small explainable recommender for saving money without cutting priorities."""
    lang = get_language()
    if not expenses:
        return {
            "summary": translate("advisor_empty_summary", lang),
            "protected": [],
            "cuts": [],
            "projected_savings": 0,
            "category_totals": [],
        }

    category_totals: dict[str, float] = defaultdict(float)
    category_importance: dict[str, list[int]] = defaultdict(list)
    category_counts: dict[str, int] = defaultdict(int)

    for expense in expenses:
        category_totals[expense["category"]] += expense["amount"]
        category_counts[expense["category"]] += 1
        category_importance[expense["category"]].append(
            IMPORTANCE_LEVELS.get(expense["importance"], 1)
        )

    max_category_total = max(category_totals.values()) or 1
    max_category_count = max(category_counts.values()) or 1
    scored_categories = []
    for category, total in category_totals.items():
        avg_importance = sum(category_importance[category]) / len(
            category_importance[category]
        )
        amount_score = total / max_category_total
        discretionary_score = (3 - avg_importance) / 2
        frequency_score = category_counts[category] / max_category_count
        priority_score = (
            (0.45 * amount_score)
            + (0.40 * discretionary_score)
            + (0.15 * frequency_score)
        )
        cut_rate = 0.05 + (0.30 * priority_score)
        recommended_cut = round(total * cut_rate, 2)
        scored_categories.append(
            {
                "category": category,
                "total": round(total, 2),
                "record_count": category_counts[category],
                "avg_importance": round(avg_importance, 2),
                "amount_score": round(amount_score, 2),
                "discretionary_score": round(discretionary_score, 2),
                "frequency_score": round(frequency_score, 2),
                "priority_score": round(priority_score, 2),
                "cut_rate": round(cut_rate * 100, 1),
                "recommended_cut": recommended_cut,
                "remaining_after_cut": round(total - recommended_cut, 2),
                "score": priority_score,
            }
        )

    scored_categories.sort(key=lambda item: item["score"], reverse=True)

    cuts = []
    protected = []
    projected_savings = 0.0
    for item in scored_categories:
        if item["avg_importance"] >= 2.5:
            protected.append(
                {
                    **item,
                    "reason": translate("reason_essential", lang),
                    "evidence": build_protected_evidence(item, lang),
                    "impact": translate("protected_impact_template", lang),
                }
            )
            continue

        if projected_savings < target_savings:
            projected_savings += item["recommended_cut"]
            cuts.append(
                {
                    **item,
                    "reason": explain_cut(item, lang),
                    "evidence": build_cut_evidence(item, lang),
                    "formula": build_cut_formula(item, lang),
                    "impact": build_cut_impact(item, lang),
                    "action_steps": build_action_steps(item, lang),
                }
            )
        else:
            protected.append(
                {
                    **item,
                    "reason": translate("reason_target_met", lang),
                    "evidence": build_protected_evidence(item, lang),
                    "impact": translate("reason_target_met", lang),
                }
            )

    if projected_savings >= target_savings:
        summary = translate("advisor_success_summary", lang).format(
            amount=f"{projected_savings:.2f}"
        )
    else:
        summary = translate("advisor_partial_summary", lang).format(
            amount=f"{projected_savings:.2f}"
        )

    return {
        "summary": summary,
        "protected": protected,
        "cuts": cuts,
        "projected_savings": round(projected_savings, 2),
        "category_totals": sorted(
            scored_categories, key=lambda item: item["total"], reverse=True
        ),
    }


def translate(key: str, lang: str | None = None) -> str:
    selected_lang = lang or "en"
    return TRANSLATIONS[selected_lang].get(key, TRANSLATIONS["en"].get(key, key))


def build_cut_evidence(item: dict, lang: str) -> str:
    return translate("evidence_template", lang).format(
        total=f"{item['total']:.2f}",
        count=item["record_count"],
        importance=f"{item['avg_importance']:.2f}",
        discretion=f"{item['discretionary_score']:.2f}",
    )


def build_cut_formula(item: dict, lang: str) -> str:
    return translate("formula_template", lang).format(
        amount_score=f"{item['amount_score']:.2f}",
        discretion_score=f"{item['discretionary_score']:.2f}",
        frequency_score=f"{item['frequency_score']:.2f}",
        priority=f"{item['priority_score']:.2f}",
        rate=f"{item['cut_rate']:.1f}",
    )


def build_cut_impact(item: dict, lang: str) -> str:
    return translate("impact_template", lang).format(
        remaining=f"{item['remaining_after_cut']:.2f}",
        cut=f"{item['recommended_cut']:.2f}",
    )


def build_protected_evidence(item: dict, lang: str) -> str:
    return translate("protected_evidence_template", lang).format(
        total=f"{item['total']:.2f}",
        importance=f"{item['avg_importance']:.2f}",
    )


def build_action_steps(item: dict, lang: str) -> list[str]:
    if item["avg_importance"] <= 1.4:
        keys = ["action_optional_1", "action_optional_2", "action_optional_3"]
    elif item["total"] >= 100:
        keys = ["action_moderate_1", "action_moderate_2", "action_moderate_3"]
    else:
        keys = ["action_small_1", "action_small_2", "action_small_3"]
    return [translate(key, lang) for key in keys]


def explain_cut(item: dict, lang: str) -> str:
    if item["avg_importance"] <= 1.4:
        return translate("reason_optional", lang)
    if item["total"] >= 100:
        return translate("reason_moderate", lang)
    return translate("reason_small", lang)


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)

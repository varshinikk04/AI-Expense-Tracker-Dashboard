import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def load_expenses():
    expenses = []
    try:
        with open("expenses.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",")
                expense = {
                    'date': parts[0],
                    'category': parts[1],
                    'amount': float(parts[2]),
                    'description': parts[3]
                }
                expenses.append(expense)
    except FileNotFoundError:
        pass
    return expenses

def save_expense(expense):
    with open("expenses.txt", "a") as file:
        file.write(
            f"{expense['date']},{expense['category']},{expense['amount']},{expense['description']}\n"
        )

st.title("💰 AI Expense Tracker")
st.subheader("Add New Expense")
date = st.text_input("Date")
category = st.text_input("Category")
amount = st.number_input(
    "Amount",
    min_value=0.0,
    step=1.0
)
description = st.text_input("Description")
if st.button("Add Expense"):
    expense = {
        'date': date,
        'category': category,
        'amount': amount,
        'description': description
    }
    save_expense(expense)
    st.success("Expense Added Successfully!")

st.subheader("Expense Records")
expenses = load_expenses()
if expenses:
    df = pd.DataFrame(expenses)
    st.dataframe(df)
else:
    st.info("No expenses found.")

def show_bar_chart(expenses):
    if len(expenses) == 0:
        st.info("No expenses found.")
        return
    category_totals = {}
    for expense in expenses:
        category = expense['category']
        amount = expense['amount']
        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount
    categories = list(category_totals.keys())
    amounts = list(category_totals.values())
    fig, ax = plt.subplots(figsize=(6, 5))
    bars = ax.bar(categories, amounts)
    ax.set_title("Expenses by Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Amount (₹)")
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2,
            height,
            f"₹{height:.0f}",
            ha='center',
            va='bottom'
        )
    st.pyplot(fig)


def show_pie_chart(expenses):
    if len(expenses) == 0:
        st.info("No expenses found.")
        return
    category_totals = {}
    for expense in expenses:
        category = expense['category']
        amount = expense['amount']
        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount
    categories = list(category_totals.keys())
    amounts = list(category_totals.values())
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.pie(
        amounts,
        labels=categories,
        autopct='%1.1f%%'
    )
    ax.set_title("Expense Distribution")
    st.pyplot(fig)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Expenses by Category")
    show_bar_chart(expenses)
with col2:
    st.subheader("Expense Distribution")
    show_pie_chart(expenses)

def ai_insights(expenses):
    if len(expenses) == 0:
        return
    total_expense = sum(
        expense['amount']
        for expense in expenses
    )
    category_totals = {}
    for expense in expenses:
        category = expense['category']
        amount = expense['amount']
        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount
    highest_category = max(
        category_totals,
        key=category_totals.get
    )
    highest_amount = category_totals[highest_category]
    percentage = (
        highest_amount / total_expense
    ) * 100
    st.subheader("🤖 AI Insights")
    st.success(
        f"Highest spending category: {highest_category}"
    )
    st.info(
        f"{highest_category} accounts for {percentage:.1f}% of total expenses."
    )
    savings = highest_amount * 0.10
    st.warning(
        f"Reducing {highest_category} spending by 10% could save ₹{savings:.2f}"
    )
ai_insights(expenses)
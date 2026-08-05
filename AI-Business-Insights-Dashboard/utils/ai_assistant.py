import pandas as pd


def answer_question(df, question):

    question = question.lower()

    # ---------------- Total Sales ----------------
    if "total sales" in question:

        if "Sales" in df.columns:

            total = df["Sales"].sum()

            return f"Total Sales = {total:,.2f}"

    # ---------------- Average Profit ----------------
    if "average profit" in question:

        if "Profit" in df.columns:

            avg = df["Profit"].mean()

            return f"Average Profit = {avg:.2f}"

    # ---------------- Highest Sales Region ----------------
    if "region" in question and "highest" in question:

        if "Region" in df.columns and "Sales" in df.columns:

            region = (
                df.groupby("Region")["Sales"]
                .sum()
                .idxmax()
            )

            value = (
                df.groupby("Region")["Sales"]
                .sum()
                .max()
            )

            return f"{region} has the highest sales ({value:,.2f})."

    # ---------------- Highest Sales Category ----------------
    if "category" in question and "highest" in question:

        if "Category" in df.columns and "Sales" in df.columns:

            category = (
                df.groupby("Category")["Sales"]
                .sum()
                .idxmax()
            )

            value = (
                df.groupby("Category")["Sales"]
                .sum()
                .max()
            )

            return f"{category} generated the highest sales ({value:,.2f})."

    # ---------------- Top Customers ----------------
    if "top" in question and "customer" in question:

        if "Customer Name" in df.columns:

            top = (
                df.groupby("Customer Name")["Sales"]
                .sum()
                .nlargest(10)
            )

            return top.to_string()

    return "Sorry, I don't understand that question yet."
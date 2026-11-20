import numpy as np
import pandas as pd


def marks_analysis(file_path):
    # 1. Load CSV data directly from file_path
    try:
        df = pd.read_csv("/analyzed_marks (1).csv")
        print(f"Data successfully loaded from '{file_path}'!\n")
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None

    # 2. Clean column headers
    df.columns = df.columns.str.strip()

    # 3. Detect subject columns (numerical columns excluding roll/id/name)
    exclude_keywords = ["roll", "id", "name"]
    subject_cols = [
        col for col in df.select_dtypes(include=[np.number]).columns
        if not any(k in col.lower() for k in exclude_keywords)
    ]

    print(f"Detected Subjects: {subject_cols}")

    if not subject_cols:
        print("No subject mark columns found for analysis.")
        return df

    # 4. Student-level calculations using NumPy
    marks_matrix = df[subject_cols].to_numpy()
    df["Total"] = np.sum(marks_matrix, axis=1)
    df["Percentage"] = np.round((df["Total"] / (len(subject_cols) * 100)) * 100, 2)

    # 5. Grade Assignment using np.select
    conditions = [
        df["Percentage"] >= 90,
        df["Percentage"] >= 80,
        df["Percentage"] >= 70,
        df["Percentage"] >= 60,
        df["Percentage"] >= 50,
        df["Percentage"] >= 40,
    ]
    grades = ["A+", "A", "B", "C", "D", "E"]
    df["Grade"] = np.select(conditions, grades, default="F")

    print("\n--- Student Performance Summary ---")
    display_cols = [c for c in ["Roll No", "Name", "Total", "Percentage", "Grade"] if c in df.columns]
    print(df[display_cols].to_string(index=False))

    # 6. Subject-level Statistics using NumPy
    stats = {
        "Subject": subject_cols,
        "Mean": [np.round(np.mean(df[sub].dropna().to_numpy()), 2) for sub in subject_cols],
        "Median": [np.median(df[sub].dropna().to_numpy()) for sub in subject_cols],
        "Std Dev": [np.round(np.std(df[sub].dropna().to_numpy()), 2) for sub in subject_cols],
        "Highest": [np.max(df[sub].dropna().to_numpy()) for sub in subject_cols],
        "Lowest": [np.min(df[sub].dropna().to_numpy()) for sub in subject_cols],
    }
    stats_df = pd.DataFrame(stats)

    print("\n--- Subject Statistics ---")
    print(stats_df.to_string(index=False))

    return df


# Specify the path directly in code (no input prompt)
file_path = "sample_marks.csv"
analyzed_df = marks_analysis(file_path)
import pandas as pd

# -------------------------------
# Load dataset
# -------------------------------
df = pd.read_csv("trains.csv")  # make sure trains.csv is in same folder
print("Dataset loaded successfully!")
print("\nFirst few rows of input data:")
print(df.head())

# -------------------------------
# Scoring Function (6 parameters)
# -------------------------------
def scoring_model(row):
    score = 0

    # 1. Fitness Certificates (20 points)
    if row['Fitness_Valid_days_left'] > 10:
        score += 20
    elif row['Fitness_Valid_days_left'] > 5:
        score += 10
    else:
        score += 2

    # 2. Job-Card Status (15 points)
    if row['JobCards_Open'] == 0:
        score += 15
    elif row['JobCards_Open'] <= 2:
        score += 8
    else:
        score += 3

    # 3. Branding Priorities (10 points)
    if row['Branding_Hours_Left'] > 50:
        score += 10
    elif row['Branding_Hours_Left'] > 20:
        score += 6
    else:
        score += 2

    # 4. Mileage Balancing (20 points)
    if row['Mileage_Remaining_km'] > 1000:
        score += 20
    elif row['Mileage_Remaining_km'] > 500:
        score += 10
    else:
        score += 3

    # 5. Cleaning & Detailing Slots (15 points)
    if row['Cleaning_Slot_Available'] == 'Yes':
        score += 15
    else:
        score += 5

    # 6. Stabling Geometry (20 points)
    if row['Stable_Position_Score'] > 0.8:
        score += 20
    elif row['Stable_Position_Score'] > 0.5:
        score += 10
    else:
        score += 4

    # Bonus: Ready for Service (extra 5 points)
    if row['Ready_For_Service'] == 'Yes':
        score += 5

    return score

# -------------------------------
# Apply Scoring
# -------------------------------
df['Readiness_Score'] = df.apply(scoring_model, axis=1)

print("\nScores calculated for each train:")
print(df[["Train_ID", "Readiness_Score"]])

# -------------------------------
# Categorization into Service / Standby / Maintenance
# -------------------------------
df = df.sort_values(by="Readiness_Score", ascending=False).reset_index(drop=True)

n = len(df)
service_count = min(int(n * 0.6), 15)    # top 60% or max 15
standby_count = min(int(n * 0.2), 5)     # next 20% or max 5
df.loc[:service_count-1, "Category"] = "Service"
df.loc[service_count:service_count+standby_count-1, "Category"] = "Standby"
df.loc[service_count+standby_count:, "Category"] = "Maintenance"

# -------------------------------
# OVERRIDE rules for JobCards
# -------------------------------
for idx, row in df.iterrows():
    if row['JobCards_Open'] >= 3:
        df.at[idx, "Category"] = "Maintenance"
    elif row['JobCards_Open'] == 2:
        df.at[idx, "Category"] = "Standby"
    # 0 or 1 → keep score-based category

# -------------------------------
# Save Results
# -------------------------------
df.to_csv("scored_trains.csv", index=False)

print("\n✅ Final categorized trains (all columns):")
print(df[["Train_ID",
          "Fitness_Valid_days_left","JobCards_Open","Branding_Hours_Left",
          "Mileage_Remaining_km","Cleaning_Slot_Available","Stable_Position_Score",
          "Ready_For_Service","Readiness_Score","Category"]])

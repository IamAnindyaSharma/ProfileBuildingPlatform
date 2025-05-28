import pandas as pd
import numpy as np
np.bool = bool  # Patch for deprecated np.bool



# Load the predefined skill dictionary from CSV
skills_df = pd.read_csv(r"C:/Users/sharm/DataFiles/skills_list.csv")
skill_list = skills_df["Skill"].str.lower().tolist()

def extract_skills(text, skill_list):
    text = text.lower()
    extracted = [skill for skill in skill_list if skill in text]
    return extracted

import os

# Define thresholds
def get_level(count):
    if count <= 2:
        return "Beginner"
    elif count <= 5:
        return "Intermediate"
    else:
        return "Advanced"

# Update skill count and level
def update_skill_tracker(extracted_skills, tracker_path=r"C:/Users/sharm/DataFiles/skills_list.csv"):
    if os.path.exists(tracker_path):
        tracker_df = pd.read_csv(tracker_path)
    else:
        tracker_df = pd.DataFrame(columns=["Skill", "Count", "Level"])

    for skill in extracted_skills:
        if skill in tracker_df["Skill"].values:
            tracker_df.loc[tracker_df["Skill"] == skill, "Count"] += 1
        else:
            new_row = pd.DataFrame([{"Skill": skill, "Count": 1}])
            tracker_df = pd.concat([tracker_df, new_row], ignore_index=True)


    # Update levels
    tracker_df["Level"] = tracker_df["Count"].apply(get_level)
    tracker_df.to_csv(tracker_path, index=False)

    return tracker_df

log = "I solved a bug in Python and ran 5 km at 6 AM."
extracted = extract_skills(log, skill_list)
updated_tracker = update_skill_tracker(extracted)
print(updated_tracker)



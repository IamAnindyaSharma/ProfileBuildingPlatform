# import pandas as pd
# import numpy as np
# import streamlit as st
# import matplotlib.pyplot as plt
# np.bool = bool  # Patch for deprecated np.bool



# # Load the predefined skill dictionary from CSV
# skills_df = pd.read_csv(r"C:/Users/sharm/DataFiles/skills_list.csv")
# skill_list = skills_df["Skill"].str.lower().tolist()

# def extract_skills(text, skill_list):
#     text = text.lower()
#     extracted = [skill for skill in skill_list if skill in text]
#     return extracted

# import os

# # Define thresholds
# def get_level(count):
#     if count <= 2:
#         return "Beginner"
#     elif count <= 5:
#         return "Intermediate"
#     else:
#         return "Advanced"

# # Update skill count and level
# def update_skill_tracker(extracted_skills, tracker_path=r"C:/Users/sharm/DataFiles/skills_tracker.csv"):
#     if os.path.exists(tracker_path):
#         tracker_df = pd.read_csv(tracker_path)
#     else:
#         tracker_df = pd.DataFrame(columns=["Skill", "Count", "Level"])

#     for skill in extracted_skills:
#         if skill in tracker_df["Skill"].values:
#             tracker_df.loc[tracker_df["Skill"] == skill, "Count"] += 1
#         else:
#             new_row = pd.DataFrame([{"Skill": skill, "Count": 1}])
#             tracker_df = pd.concat([tracker_df, new_row], ignore_index=True)


#     # Update levels
#     tracker_df["Level"] = tracker_df["Count"].apply(get_level)
#     tracker_df.to_csv(tracker_path, index=False)

#     return tracker_df



# def save_log_entry(log, extracted, log_path=r"C:/Users/sharm/DataFiles/log_history.csv"):
#     log_df = pd.DataFrame([{
#         "Date": pd.Timestamp.now(),
#         "Log": log,
#         "Extracted Skills": ", ".join(extracted)
#     }])
    
#     if os.path.exists(log_path):
#         existing_df = pd.read_csv(log_path)
#         updated_df = pd.concat([existing_df, log_df], ignore_index=True)
#     else:
#         updated_df = log_df

#     updated_df.to_csv(log_path, index=False)
    

# def show_skill_dashboard(tracker_path=r"C:/Users/sharm/DataFiles/skills_tracker.csv"):
#     st.subheader("📊 Your Skill Progression")
#     if os.path.exists(tracker_path):
#         df = pd.read_csv(tracker_path)
#         if df.empty:
#             st.warning("⚠️ Skill tracker file is empty.")
#             return
#         df = df.sort_values(by="Count", ascending=False)
#         st.dataframe(df)

#         fig, ax = plt.subplots()
#         ax.barh(df["Skill"], df["Count"], color="skyblue")
#         ax.set_xlabel("Frequency")
#         ax.set_title("Skills You've Demonstrated")
#         st.pyplot(fig)
#     else:
#         st.error("❌ Tracker file not found. Submit a log first.")

        

# log_input = st.text_area("What did you do today?")
# if st.button("Submit"):
#     extracted = extract_skills(log_input, skill_list)
#     update_skill_tracker(extracted)
#     save_log_entry(log_input, extracted)
#     st.success("Skills extracted: " + ", ".join(extracted))

# show_skill_dashboard()

import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

np.bool = bool  # For deprecated np.bool

# File paths
SKILL_LIST_PATH = r"C:/Users/sharm/DataFiles/skills_list.csv"
TRACKER_PATH = r"C:/Users/sharm/DataFiles/skills_tracker.csv"
LOG_HISTORY_PATH = r"C:/Users/sharm/DataFiles/log_history.csv"

# Load skills
skills_df = pd.read_csv(SKILL_LIST_PATH)
skill_list = skills_df["Skill"].str.lower().tolist()

# Skill level thresholds
def get_level(count):
    if count <= 2:
        return "Beginner"
    elif count <= 5:
        return "Intermediate"
    else:
        return "Advanced"

# Skill extraction
def extract_skills(text, skill_list):
    text = text.lower()
    return [skill for skill in skill_list if skill in text]

# Update skill tracker
def update_skill_tracker(extracted_skills):
    if os.path.exists(TRACKER_PATH):
        tracker_df = pd.read_csv(TRACKER_PATH)
    else:
        tracker_df = pd.DataFrame(columns=["Skill", "Count"])

    for skill in extracted_skills:
        if skill in tracker_df["Skill"].values:
            tracker_df.loc[tracker_df["Skill"] == skill, "Count"] += 1
        else:
            new_row = pd.DataFrame([{"Skill": skill, "Count": 1}])
            tracker_df = pd.concat([tracker_df, new_row], ignore_index=True)

    tracker_df["Level"] = tracker_df["Count"].apply(get_level)
    tracker_df.to_csv(TRACKER_PATH, index=False)
    return tracker_df

# Save daily log
def save_log_entry(log, extracted):
    log_df = pd.DataFrame([{
        "Date": pd.Timestamp.now(),
        "Log": log,
        "Extracted Skills": ", ".join(extracted)
    }])

    if os.path.exists(LOG_HISTORY_PATH):
        existing_df = pd.read_csv(LOG_HISTORY_PATH)
        updated_df = pd.concat([existing_df, log_df], ignore_index=True)
    else:
        updated_df = log_df

    updated_df.to_csv(LOG_HISTORY_PATH, index=False)

# Dashboard display
def show_skill_dashboard():
    if not os.path.exists(TRACKER_PATH):
        st.info("Submit a log to generate your skill dashboard.")
        return

    df = pd.read_csv(TRACKER_PATH)
    if df.empty:
        st.warning("No skills tracked yet.")
        return

    df = df.sort_values(by="Count", ascending=False)
    st.subheader("📊 Your Skill Progression")
    st.dataframe(df, use_container_width=True)

    # ✅ No matplotlib used here
    st.bar_chart(data=df.set_index("Skill")["Count"])



# ---------- Streamlit App ----------
st.title("🧠 Work Journal → Real Skills Tracker")

log_input = st.text_area("📝 What did you do today?")

if st.button("Submit"):
    extracted = extract_skills(log_input, skill_list)
    if extracted:
        update_skill_tracker(extracted)
        save_log_entry(log_input, extracted)
        st.success(f"✅ Skills extracted: {', '.join(extracted)}")
        show_skill_dashboard()
    else:
        st.warning("No matching skills found in your log.")



# Manual debug
st.write("DEBUG MODE:")
st.write("📊 Dashboard is running...")

if os.path.exists(TRACKER_PATH):
    st.success("✅ Tracker file FOUND!")
    debug_df = pd.read_csv(TRACKER_PATH)
    st.write("📂 Tracker DataFrame Preview:")
    st.write(debug_df)
else:
    st.error("❌ Tracker file NOT FOUND!")

# DEBUG DASHBOARD CHECK
st.subheader("🧪 Debug Dashboard Check")
if os.path.exists(TRACKER_PATH):
    st.success("✅ Found skills_tracker.csv!")
    try:
        df = pd.read_csv(TRACKER_PATH)
        st.write("🔍 Tracker file contents:")
        st.write(df)

        if df.empty:
            st.warning("⚠️ The tracker file is empty.")
        else:
            st.success("✅ Tracker file has data!")
            fig, ax = plt.subplots()
            ax.barh(df["Skill"], df["Count"], color="skyblue")
            ax.set_xlabel("Frequency")
            ax.set_title("Skills You've Demonstrated")
            st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Error reading CSV: {e}")
else:
    st.error("❌ File not found: skills_tracker.csv")



    

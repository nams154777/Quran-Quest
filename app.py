import streamlit as st
from supabase import create_client

# TEST: Zeigt uns, ob die URL ankommt (OHNE den geheimen Key zu zeigen)
if "SUPABASE_URL" in st.secrets:
    st.write(f"URL geladen: {st.secrets['SUPABASE_URL'][:10]}...") 
else:
    st.error("FEHLER: SUPABASE_URL wurde in den Secrets nicht gefunden!")

url = st.secrets.get("SUPABASE_URL", "")
key = st.secrets.get("SUPABASE_KEY", "")

# Falls Leerzeichen mitkopiert wurden, entfernen:
url = url.strip()
key = key.strip()

supabase = create_client(url, key)

st.set_page_config(page_title="Ramadan Quran Quest", page_icon="🌙")

# -- UI & LOGIK --
st.title("🌙 Ramadan Quran Quest")
st.subheader("Your Road to Success")

# 1. Profil-Setup
name = st.text_input("Your Name", "Ahi")
goal = st.radio("Dein Ziel pro Tag:", [5, 7], help="5 Qur'an oder 7 Qur'an Intensiv")

# 2. Fortschritt-Eingabe
st.divider()
juz_today = st.number_input("How many Juz did you read today?", min_value=0, max_value=30)

if st.button("Fortschritt speichern 🚀"):
    # Logik für Belohnungssystem
    points = juz_today * 10
    bonus = 50 if juz_today >= goal else 0
    
    # Speichern in Datenbank
    data = {"username": name, "juz_completed": juz_today, "goal_type": goal}
    supabase.table("quran_tracker").insert(data).execute()
    
    st.success(f"Awesome! You earned {points + bonus} points!")
    if bonus > 0:
        st.balloons()
        st.info("🏆 BADGE EARNED: 'Daily Warrior'")

# 3. Community Leaderboard
st.divider()
st.write("### 📊 Global Leaderboard")

# Hier werden die Daten aus Supabase abgerufen und als Tabelle angezeigt


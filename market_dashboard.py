import streamlit as st
from streamlit_autorefresh import st_autorefresh
import matplotlib.pyplot as plt
import datetime as dt
import pytz

# Auto-refresh every 60 seconds
st_autorefresh(interval=60 * 1000, key="refresh")

# Timezone: Asia/Kolkata (IST)
IST = pytz.timezone("Asia/Kolkata")
now = dt.datetime.now(IST)  # force IST

# Market dataset: (Name, Start, End in minutes since 05:00, Region)
markets = [
    ("Tokyo", 30, 390, "Asia"),
    ("Australia", 30, 390, "Asia"),
    ("Singapore", 90, 510, "Asia"),
    ("Shanghai", 120, 450, "Asia"),
    ("Hong Kong", 120, 510, "Asia"),
    ("India", 255, 630, "India"),
    ("London", 510, 1020, "Europe"),
    ("Frankfurt", 510, 1020, "Europe"),
    ("New York", 900, 1230, "US"),
    ("Toronto", 900, 1230, "US"),
]

region_colors = {
    "Asia": "skyblue",
    "India": "green",
    "Europe": "orange",
    "US": "red"
}

st.title("🌍 Global Market Hours (IST)")

# Minutes since 05:00 IST (wrap across midnight)
minutes_since_5am = (now.hour * 60 + now.minute) - 300
if minutes_since_5am < 0:
    minutes_since_5am += 1440

fig, ax = plt.subplots(figsize=(12,6))
ax.set_xlim(0, 1320)
ax.set_ylim(0, len(markets))
ax.set_xlabel("IST Time")
ax.set_ylabel("Markets")

# Add hourly ticks from 05:00 to 03:00 next day
ticks = list(range(0, 1321, 60))  # every 60 minutes
labels = []
for t in ticks:
    hour = (5 + t // 60) % 24
    labels.append(f"{hour:02d}:00")
ax.set_xticks(ticks)
ax.set_xticklabels(labels, rotation=0)

for i, (name, start, end, region) in enumerate(markets):
    ax.barh(i, end-start, left=start, color=region_colors[region], alpha=0.6)
    ax.text(start, i, f"{start//60+5}:{start%60:02d}", va="center", ha="right")
    ax.text(end, i, f"{end//60+5}:{end%60:02d}", va="center", ha="left")

# Current time line
ax.axvline(minutes_since_5am, color="yellow", lw=3)

# Legend overlay
handles = [plt.Rectangle((0,0),1,1, color=color) for color in region_colors.values()]
labels = list(region_colors.keys())
ax.legend(handles, labels, title="Regions", loc="upper right")

st.pyplot(fig)
st.write(f"🕒 Current IST Time: {now.strftime('%H:%M')}")

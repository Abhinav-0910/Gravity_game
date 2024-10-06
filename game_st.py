import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page title and favicon
st.set_page_config(page_title="Gravity Collector Game", page_icon="🚀")

# Title and introduction
st.title("🌌 Gravity Collector Game")
st.write("Welcome to the Gravity Collector Game! Explore different planets and collect coins while experiencing varying gravity levels.")

# Game description
st.header("About the Game")
st.write("""
In Gravity Collector, you play as an astronaut exploring different planets in our solar system. 
Your mission is to collect as many coins as possible while adapting to each planet's unique gravity.
Jump, move, and time your actions carefully to succeed!
""")

# Planet selection
st.header("Choose Your Planet")
planet = st.selectbox("Select a planet to explore:", 
                      ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"])

# Planet information
planet_info = {
    "Mercury": {"gravity": 3.7, "color": "#808080"},
    "Venus": {"gravity": 8.87, "color": "#FFC649"},
    "Earth": {"gravity": 9.81, "color": "#00FF00"},
    "Mars": {"gravity": 3.721, "color": "#FF0000"},
    "Jupiter": {"gravity": 24.79, "color": "#FF8C00"},
    "Saturn": {"gravity": 10.44, "color": "#EEE8AA"},
    "Uranus": {"gravity": 8.69, "color": "#ADD8E6"},
    "Neptune": {"gravity": 11.15, "color": "#0000FF"}
}

st.subheader(f"Planet: {planet}")
st.write(f"Gravity: {planet_info[planet]['gravity']} m/s²")

# Visualize gravity comparison
st.subheader("Gravity Comparison")
gravity_data = pd.DataFrame.from_dict(planet_info, orient='index')
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(gravity_data.index, gravity_data['gravity'], color=gravity_data['color'])
ax.set_ylabel("Gravity (m/s²)")
ax.set_title("Gravity on Different Planets")
plt.xticks(rotation=45)
st.pyplot(fig)

# Player weight input
st.header("Player Information")
weight = st.slider("Enter your weight (kg):", min_value=30, max_value=200, value=70, step=1)
st.write(f"Your weight on Earth: {weight} kg")
st.write(f"Your weight on {planet}: {weight * planet_info[planet]['gravity'] / 9.81:.2f} kg")

# Game tips
st.header("Game Tips")
st.write("""
- Use the arrow keys to move left and right
- Press the spacebar to jump
- Collect as many coins as possible before the timer runs out
- Adapt your movements to the planet's gravity
- Complete all levels to win the game
""")

# Call to action
st.header("Ready to Play?")
st.write("Download the Gravity Collector game and start your interplanetary adventure!")
if st.button("Download Game"):
    st.write("Thank you for your interest! The download link will be available soon.")

# Footer
st.markdown("---")
st.write("Developed by [Your Name/Team]. Powered by Pygame and Streamlit.")
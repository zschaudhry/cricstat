import streamlit as st
import plotly.express as px
import numpy as np
import requests
from bs4 import BeautifulSoup
import pandas as pd

# --- Utility Functions ---

def fetch_player_stats(num_records=50):
    """Scrape T20I batting records from ESPN Cricinfo."""
    base_url = "https://stats.espncricinfo.com/ci/engine/stats/index.html"
    all_players, all_seasons, all_matches, all_innings, all_not_outs = [], [], [], [], []
    all_runs, all_high_score, all_average, all_balls_faced, all_strike_rate = [], [], [], [], []
    all_hundreds, all_fifties, all_zeros, all_fours, all_sixes = [], [], [], [], []

    for start in range(1, num_records + 1, 50):
        params = {
            "class": 3,
            "template": "results",
            "type": "batting",
            "start": start
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        try:
            response = requests.get(base_url, headers=headers, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            st.error(f"Request error: {e}")
            return None

        soup = BeautifulSoup(response.content, 'html.parser')
        tables = soup.find_all('table', class_='engineTable')
        if len(tables) < 3:
            st.error("Unable to find player statistics data table.")
            return None
        data_table = tables[2]

        for row in data_table.find_all('tr')[1:]:
            cols = row.find_all('td')
            if len(cols) >= 15:
                all_players.append(cols[0].text.strip())
                all_seasons.append(cols[1].text.strip())
                all_matches.append(cols[2].text.strip())
                all_innings.append(cols[3].text.strip())
                all_not_outs.append(cols[4].text.strip())
                all_runs.append(cols[5].text.strip())
                all_high_score.append(cols[6].text.strip())
                avg = cols[7].text.strip()
                all_average.append(None if avg == '-' or avg == '' else avg)
                all_balls_faced.append(cols[8].text.strip())
                all_strike_rate.append(cols[9].text.strip())
                all_hundreds.append(cols[10].text.strip())
                all_fifties.append(cols[11].text.strip())
                all_zeros.append(cols[12].text.strip())
                all_fours.append(cols[13].text.strip())
                all_sixes.append(cols[14].text.strip())
            if len(all_players) >= num_records:
                break
        if len(all_players) >= num_records:
            break

    df = pd.DataFrame({
        'Player': all_players[:num_records],
        'Season': all_seasons[:num_records],
        'Matches': all_matches[:num_records],
        'Innings': all_innings[:num_records],
        'Not Outs': all_not_outs[:num_records],
        'Runs': all_runs[:num_records],
        'High Score': all_high_score[:num_records],
        'Average': all_average[:num_records],
        'Balls Faced': all_balls_faced[:num_records],
        'Strike Rate': all_strike_rate[:num_records],
        '100s': all_hundreds[:num_records],
        '50s': all_fifties[:num_records],
        '0s': all_zeros[:num_records],
        '4s': all_fours[:num_records],
        '6s': all_sixes[:num_records]
    })
    df.index = df.index + 1  # Start index from 1 instead of 0
    return df



# --- Streamlit App ---

st.set_page_config(page_title="T20 International Batting Records", layout="wide")
st.title("🏏 T20 International Batting Records")

st.markdown(
    """
    Explore top T20 International batting records.  
    - Use the slider below to select how many players to display.
    - Scroll the table horizontally to view all stats (matches, runs, strike rate, 100s, 50s, etc).
    - Click on column headers to sort the table.
    - The bar chart below shows total runs for the selected players.
    """,
    unsafe_allow_html=True
)

# Add a container to control the width of the slider to match the table width
slider_col, _ = st.columns([6, 4])  # Adjust the ratio as needed to match table width
with slider_col:
    num_records = st.slider(
        "Number of records to display",
        min_value=10,
        max_value=200,
        value=20,
        step=10
    )

player_stats = fetch_player_stats(num_records)

if player_stats is not None:
    st.subheader("Player Batting Statistics")
   
    st.write(player_stats)

    # Plot player runs
    player_stats['Runs'] = pd.to_numeric(player_stats['Runs'].astype(str).str.replace(',', ''), errors='coerce')
    fig = px.bar(
        player_stats.head(num_records),
        x='Player',
        y='Runs',
        title=f'Top {num_records} Player Runs',
        template='plotly_white'
    )
    fig.update_layout(xaxis_tickangle=-45, height=500)
    st.plotly_chart(fig, use_container_width=True)

    # Create a scatter plot
    def create_scatter_plot(player_stats):
        fig = px.scatter(player_stats, x='Average', y='Strike Rate', hover_name='Player', title='Average vs Strike Rate')
        return fig

    
    fig = create_scatter_plot(player_stats)
    # Display the scatter plot
    st.plotly_chart(fig, use_container_width=True)

    # create a sunburst chart
    def create_sunburst_chart(player_stats):
        fig = px.sunburst(
            player_stats.head(10),
            path=['High Score', 'Average', 'Runs', 'Innings', 'Matches', 'Player'],
            values='Strike Rate',
            color='Player',
            color_continuous_scale='RdBu',
            color_continuous_midpoint=np.average(player_stats['Matches'].astype(float)),
            hover_data=['High Score', 'Average'],
            title='High Scores by Player and Matches',
            template='plotly_white'
        )
        return fig

    fig = create_sunburst_chart(player_stats)
    fig.update_layout(width=900, height=700)
    # Display the sunburst chart
    st.plotly_chart(fig, use_container_width=True)

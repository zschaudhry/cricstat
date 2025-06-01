# T20 International Batting Records Dashboard

This project is a Streamlit web application that displays and visualizes top T20 International cricket batting records. The dashboard scrapes live data from ESPN Cricinfo and provides interactive charts and tables for cricket enthusiasts and analysts.

## Features

- **Live Data:** Scrapes the latest T20I batting stats from ESPN Cricinfo.
- **Interactive Table:** View, scroll, and sort batting records.
- **Customizable Display:** Use a slider to select how many player records to display (10–200).
- **Visualizations:**
  - Bar chart of player runs.
  - Scatter plot of Average vs Strike Rate.
  - Sunburst chart for high scores and player breakdowns.
- **Responsive Layout:** Optimized for wide screens and horizontal scrolling.

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/cricstat.git
    cd cricstat
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Streamlit app:**
    ```bash
    streamlit run cricket_dashboard.py
    ```

2. **Open your browser:**  
   The app will open automatically or you can visit [http://localhost:8501](http://localhost:8501).

## File Structure

- `cricket_dashboard.py` — Main Streamlit app and scraping logic.
- `requirements.txt` — Python dependencies.

## Screenshot

 <img width="670" alt="cricDash" src="https://github.com/user-attachments/assets/2d10d5d5-6fd0-423c-895d-8c28ef631fe5" />


## Notes

- The app scrapes data live from ESPN Cricinfo. If the website structure changes, the scraper may need updates.
- For best experience, use the app on a desktop or wide screen.

## License

MIT License

---

**Made with ❤️ using [Streamlit](https://streamlit.io/) and [Plotly](https://plotly.com/python/).**

# Youtube Channel Tracker(Physics Wallah Analytics)

This project is an end-to-end data analytics pipeline that extracts, processes, and visualizes the Physics Wallah YouTube channel data using Python, MySQL, and Power BI

## Problem Statement

Analyzing YouTube channel performance manually is inefficient and time-consuming.  
This project automates data extraction, storage, and visualization to provide actionable insights into video performance, engagement trends, and publishing patterns.

## Dashboard Preview

[![Dashboard](dashboard/dashboard.png)](dashboard/pw_visuals.pbix)

## Project Highlights

- Built an end-to-end data pipeline using the YouTube Data API
- Automated data collection using Python scripts
- Stored structured data in a MySQL database
- Designed an interactive Power BI dashboard
- Analyzed video performance, trends, and engagement metrics

## Results

- Processed 1600+ videos dataset
- Analyzed 3B+ total views and 90M+ likes
- Identified high-performing content patterns
- Built an interactive dashboard with filters and KPIs

## Tech Stack

- Python (requests, pandas, isodate)
- MySQL
- Power BI
- YouTube Data API

## Project Structure

- 'src/' -> Python source files
- 'data/' -> CSV output file
- 'dashboard/' -> Power BI dashboard
- 'database/' -> MySQL schema file

## Workflow

- YouTube API -> Python Scripts -> MySQL Database -> CSV -> Power BI dashboard

## Key Insights

- Identified top-performing videos based on views and likes
- Found engagement ratio trends (Likes/Views)
- Analyzed upload frequency pattern over time
- Discovered peak publishing periods for higher engagement

## How to Run

1. Clone the repository
2. Install dependencies: pip install -r requirements.txt
3. Add your YouTube API key to the script
4. Run the Python scripts: python src/api.py -> python src/data_fetching.py 
5. Check the generated CSV in 'data/'
6. Import schema from `database/schema.sql` into MySQL
7. Open Power BI dashboard from `dashboard/pw_visuals.pbix`

## Future Improvements

- Deploy dashboard online (Power BI Service)
- Add sentiment analysis on video comments
- Build a web dashboard using Streamlit

## Author

Akshat Jain  
Aspiring Data Analyst | Python | SQL | Power BI

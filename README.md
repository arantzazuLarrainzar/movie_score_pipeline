# Movie Score Data Pipeline

## About the project
This project is an application that consists in two parts, a first that is a pipeline that ingests, cleans, standarizes and combines movie data from different providers, and a second one that allows the user to query information of a movie.

Currently the application ingests data from three different providers, but it is implemented in a way that is possible to add new methods for the extraction of data of new providers or modifying the current ones if the format changes.

## Built with
This application was implemented with the language python and the library used is `pandas`.

## Getting Started

### Prerequisites
The library `pandas` must be installed for the correct funtionality of the project:

### Installation
1. Clone the repo
```
git clone https://github.com/arantzazuLarrainzar/movie_score_pipeline.git
```
2. Install the `pandas` library
```
pip install pandas
```
3. Enter in the repo and run the following command, the app will start and ask which task to execute
```
cd movie_score_pipeline
python3 app.py
```

## Usage
```
>>> python3 app.py
Enter the option you want execute, (a) update the database, (b) query the information of a movie or (c) close the application: a
The database has been updated.

Enter the option you want execute, (a) update the database, (b) query the information of a movie or (c) close the application: b
Introduce the title of the movie: Inception
Introduce the release year of the movie: 2010

The film Inception, released in the year 2010, has the following features:
	critic_score_percentage: 87.0
	top_critic_score: 8.1
	total_critic_reviews_counted: 450.0
	audience_average_score: 9.1
	total_audience_ratings: 1500000.0
	international_box_office_gross: 535700000.0
	production_budget_usd: 160000000.0
	marketing_spend_usd: 100000000.0
	domestic_box_office_gross: 292576195.0

Enter the option you want execute, (a) update the database, (b) query the information of a movie or (c) close the application: b
Introduce the title of the movie: Toy Story 2
Introduce the release year of the movie: 1999
The film is not in the database

Enter the option you want execute, (a) update the database, (b) query the information of a movie or (c) close the application: c
The application is turning off.
```

## Roadmap

- [x] Establish an architecture for the project.
- [x] Implement the test methods.
- [x] Implement the needed methods for the project.
- [x] Implement the app to access the different options.
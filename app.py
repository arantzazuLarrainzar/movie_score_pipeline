from pipeline import DataPipeline
import pandas as pd


if __name__ == "__main__":
    """
    Application that allows users to interact with the database by uploading
    the new information from providers or querying any information about a
    movie.
    """
    # get our movie score data pipeline
    pipe = DataPipeline()
    # start the app
    cont = True
    while(cont):
        # query option to execute
        option = input(
            "Enter the option you want execute, (a) update the database, (b)"\
            " query the information of a movie or (c) close the application: ")
        if option == "a":
            # update the database
            pipe.update()
            print("The database has been updated.\n")
        elif option == "b":
            # get information of a movie, query title and release year
            title = input("Introduce the title of the movie: ")
            year = input("Introduce the release year of the movie: ")
            try:
                year = int(year)
                movie: pd.Series = pipe.get(movie_title=title, release_year=year)
                if movie.empty:
                    print("The film is not in the database\n")
                else:
                    print("\nThe film {}, released in the year {}, has the following features:".format(title, year))
                    for feat, data in movie.items():
                        print("\t{}: {}".format(feat, data))
                    print()
            except ValueError:
                print("The introduced year is incorrect, it must be an integer.\n")
        elif option == "c":
            # turn off the application
            print("The application is turning off.")
            cont = False
        else:
            print("The introduced option is not correct.\n")

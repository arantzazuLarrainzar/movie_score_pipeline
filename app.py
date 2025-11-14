from modules import DataPipeline
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
            "Enter the option you want to execute:\n   (a) update the database "\
            "with the data supplied by all the providers\n   (b) update the "\
            "database with the data given by one supplier\n   (c) query the "\
            "information of a movie\n   (d) close the application\n")
        if option == "a":
            # update the database with the data given by all the providers
            pipe.run_all_providers()
            print(
                "The database has been updated with the information given by "\
                "each provider.\n")
        elif option == "b":
            # update the database with the info of one provider
            provider = input(
                "Enter the name of the provider [provider1/provider2/"\
                "provider3]: ")
            pipe.run_one_provider(provider)
            print(
                "The database has been updated with the information of the "\
                f"provider: {provider}.\n")
        elif option == "c":
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
        elif option == "d":
            # turn off the application
            print("The application will shut down.")
            cont = False
        else:
            print("The introduced option is not correct.\n")

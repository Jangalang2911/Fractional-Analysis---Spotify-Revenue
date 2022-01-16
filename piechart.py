""" This is the file containing documentation regarding plotting of the piechart
"""
import matplotlib.pyplot as plt
import main


def parallel_lists_of_genres_and_streams(
        genre_streams: list[tuple[dict[str, int], list[main.Spotify]]]) -> (list, list):
    """ Converts the provided list into two parallel lists, one including the name of each genre,
    and the other including the number of streams of each genre
    """
    num_songs_by_genre = []
    name_genre = []
    for i in range(len(genre_streams)):
        for genre in genre_streams[i][0]:
            name_genre.append(genre)
            num_songs_by_genre.append(genre_streams[i][0][genre])

    return name_genre, num_songs_by_genre


def calculate_percentages(genres: list[list[dict[str, int], list[main.Spotify]]]) -> dict:
    """ Calculates percentage of streams that each genre had out of the sum of the all streams
    among all genres
    """
    genres_to_streams = {}
    percentage_per_genre = {}
    sum_streams = 0
    for i in range(len(genres)):
        for genre in genres[i][0]:
            genres_to_streams[genre] = genres[i][0][genre]
            sum_streams += genres[i][0][genre]

    for genre in genres_to_streams:
        percentage_per_genre[genre] = float("{:.2f}".format((genres_to_streams[genre] / sum_streams) * 100))

    return percentage_per_genre


def genre_titles_with_percentages(percentages_per_genre: dict) -> (list, list):
    """Updates the name of each genre with its corresponding percentage, to include it
    in each genre's name for the legend of the pie chart
    """
    updated_names = []
    percentages = []

    for genre in percentages_per_genre:
        updated_names.append(genre + ', ' + str(percentages_per_genre[genre]) + '%')
        percentages.append(percentages_per_genre[genre])

    return updated_names, percentages


def piechart() -> None:
    """ Shows the piechart produced from the data analysis
    """
    genre_labels_and_percentages = genre_titles_with_percentages(calculate_percentages(
        main.categorise_by_genre(main.read_spotify_200('spotify.csv'))))

    patches, _ = plt.pie(genre_labels_and_percentages[1], colors=main.colours)

    plt.legend(patches, genre_labels_and_percentages[0], title="genre", loc="upper right",
               prop={'size': 6}, bbox_to_anchor=(1.25, 1))

    plt.show()

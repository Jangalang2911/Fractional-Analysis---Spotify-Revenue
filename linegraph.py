""" The purpose of this python file is to plot the line graph which plots
a separate line for each music genre, and takes year as the x-axis,
and the number of times a song from that genre occurred in the weekly
Spotify top 200 Global dataset.
"""
import matplotlib.pyplot as plt
import numpy as np
import main


def find_genre_count_for_year(year: int) -> list[dict[str: int]]:
    """ Calculates the count of the number of songs for each genre that appeared in the top 200
    for the specified year. Produces a list of dictionaries which map each genre to its respective
    count of appearances within the top 200.
    """
    year_difference = year - 2017
    genre_filtered = main.categorise_by_genre(main.categorise_by_year(
        main.read_spotify_200('spotify.csv'))[year_difference])
    genre_count_list = []
    for j in range(len(genre_filtered)):
        genre_count_list.append(genre_filtered[j][0])
    return genre_count_list


def get_genre_lists() -> list[list]:
    """ This function creates a list of lists. There are 26 lists within the outer list, one for
    each genre considered for the line graph. Each genre's list contains 4 elements, which are the
    number of songs of that genre for each year in the years 2017 to 2020.
    """
    expanded_list = []
    for genre_index in range(26):
        for year in range(2017, 2021):
            genre_count = find_genre_count_for_year(year)
            m = [genre_count[genre_index][item] for item in genre_count[genre_index]]
            n = m[0]
            expanded_list.append(n)
    genre_list = []
    splits = np.array_split(expanded_list, 26)
    for array in splits:
        genre_list.append(list(array))
    return genre_list


def linegraph() -> None:
    """ This function generates a line graph to represent the line corresponding to each genre's
    number of appearances in the top 200 Spotify global songs for the years 2017 to 2020.
    """
    year_list = [2017, 2018, 2019, 2020]

    for n in range(26):
        plt.plot(year_list, get_genre_lists()[n], linewidth=3, label=main.Genres[n],
                 color=main.colours[n])

    plt.gca().legend(loc='upper right', bbox_to_anchor=(1, 1), ncol=2, prop={'size': 8})

    plt.xticks([2017, 2018, 2019, 2020])

    plt.xlabel('Year')
    plt.ylabel('Genre Occurrence Count')

    plt.show()

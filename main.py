""" This is the main file of the Spotify data analysis
"""
from dataclasses import dataclass
import csv


@dataclass
class Spotify:
    """
    A datatype representing certain things in Spotify that would help make sense of data.

    This corresponds to one row of the tabular data found in Spotify Top 200 Global (2017-2021).csv

    Attributes:
    - Rank: Rank on Spotify Top 200 charts
    - Track: Name of Track
    - Artist: Name of Artist
    - Streams: No. of streams at that time
    - Link: link to song
    - Week: The week of the year
    - Album_Name: Name of the album
    - Duration_MS: Duration of song in millisecond
    - Explicit: Whether song is explicit or not
    - Track_No: Track number on the album
    - Artist_Followers: Number of Followers the artist has
    - Artist_Genres: The genres the artist falls under

    Representation invariants:
    - 1 <= Rank <= 200
    - Explicit in {'TRUE', 'FALSE'}
    """
    Rank: int
    Track: str
    Artist: str
    Streams: int
    Link: str
    Week: str
    Album_Name: str
    Duration_MS: int
    Explicit: str
    Track_No: int
    Artist_Followers: int
    Artist_Genres: list[str]


Genres = ['pop', 'hip hop', 'edm', 'electro', 'soul', 'r&b', 'reggae', 'dance', 'trap', 'tropical',
          'rap', 'rock', 'girl group', 'latin', 'southern', 'uk', 'australian', 'emo', 'sad',
          'k-pop', 'funk', 'boy band', 'atl', 'post-teen', 'viral', 'canadian']


colours = ['#000000', '#808080', '#F08080', '#800000', '#FF0000', '#F4A460', '#DEB887', '#FFA500',
           '#DAA520', '#F0E68C', '#808000', '#9ACD32', '#556B2F', '#00FF00', '#7FFFD4', '#AFEEEE',
           '#2F4F4F', '#5F9EA0', '#00FFFF', '#87CEEB', '#1E90FF', '#7B68EE', '#4B0082', '#D8BFD8',
           '#FF69B4', '#8B4513']


def string_to_list(string: str) -> list[str]:
    """
    This function is designed to take the string which contains the list of genres corresponding to
    the artist of one song as an input, and output the list of genres in a list of strings format,
    where each string in the list is a genre.
    """
    if string == "[]":  # check if the genre list is empty
        return []
    elif string[0] == '[':  # check if the genre list starts with open bracket ([)
        split_string = string.split("'")
        split_string.pop(-1)
        split_string.pop(0)
        for i in range(len(split_string)):
            if i in range(len(split_string)):
                if split_string[i] == ", ":
                    split_string.pop(i - len(split_string))
            else:
                return split_string
    else:  # this else statement is for genre lists that start with double inverted and bracket ("[)
        split_string = string.split("'")
        split_string.pop(-1)
        split_string.pop(-1)
        split_string.pop(0)
        split_string.pop(0)
        for i in range(len(split_string)):
            if i in range(len(split_string)):
                if split_string[i] == ", ":
                    split_string.pop(i - len(split_string))
            else:
                return split_string


def read_spotify_200(filename: str) -> list[Spotify]:
    """
    Reads each row of the csv file and assigns the current rows data to the attributes of the
    Spotify dataclass.
    """
    input_so_far = []
    with open(filename) as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        for row in reader:
            input_so_far.append(Spotify(int(row[0]), row[1], row[2], int(row[3]), row[4], row[5],
                                        row[6], int(row[7]), row[8], int(row[9]), int(row[10]),
                                        string_to_list(row[11])))

    return input_so_far


def read_spotify_regression_data(str1: str, str2: str, str3: str) -> dict[str: (int, int, int)]:
    """
    Read the revenue, users, and subscription csv files
    """
    dict_revenue = {}
    with open(str1) as file:
        reader = csv.reader(file, delimiter=',')
        for _ in range(5):
            next(reader)
        for row in reader:
            dict_revenue[row[0]] = int(row[1])

    dict_premium = {}
    with open(str2) as file:
        reader = csv.reader(file, delimiter=',')
        for _ in range(9):
            next(reader)
        for row in reader:
            dict_premium[row[0]] = int(row[1])

    dict_regular = {}
    with open(str3) as file:
        reader = csv.reader(file, delimiter=',')
        for _ in range(9):
            next(reader)
        for row in reader:
            dict_regular[row[0]] = int(row[1])

    list_revenue = [dict_revenue[items] for items in dict_revenue]
    list_premium = [dict_premium[items] for items in dict_premium]
    list_regular = [dict_regular[items] for items in dict_regular]

    final_dict = {}
    for item in dict_revenue:
        for i in range(len(list_revenue)):
            if dict_revenue[item] == list_revenue[i]:
                final_dict[item] = (list_revenue[i], list_premium[i], list_regular[i])
    return final_dict


def categorise_by_year(lst_total: list[Spotify]) -> list[list[Spotify]]:
    """
    Takes the list of provided Spotify songs and returns a list which has nested lists for each
    year's songs that appeared in the weekly Top 200 Spotify Global chart.
    """
    lists_by_year = []
    for _ in range(5):
        lists_by_year.append([])

    for i in range(5):
        for each_song in lst_total:
            if str(i + 2017) in each_song.Week:
                lists_by_year[i].append(each_song)

    return lists_by_year


def categorise_by_genre(lst: list[Spotify]) -> list[list[dict[str, int], list[Spotify]]]:
    """
    Categorises songs by genre; returns a list of tuples, where each tuple consists of:
      1. a dictionary which maps the genre to the number of songs with that genre
        (in the provided list)
      2. the list of songs in the given genre

    Argument can be either the entire list of Songs, or the list of Songs for a given year
    """
    final_lst = []
    for _ in range(len(Genres)):
        final_lst.append([])

    for genre in Genres:
        tup1 = {genre: 0}  # 1st element of the tuple
        tup2 = []  # 2nd element of the tuple

        for each_song in lst:
            if genre in str(each_song.Artist_Genres):
                tup2.append(each_song)

        tup1[genre] = len(tup2)

        # A way around the lack of an index; for each genre, its corresponding information is
        # mapped to the same index the genre has in the list Genres, creating parallelism between
        # the lists
        final_lst[Genres.index(genre)].append(tup1)
        final_lst[Genres.index(genre)].append(tup2)

    return final_lst

"""
This is the CS Project's First File
"""
from dataclasses import dataclass
import csv

#Global variable consisting of all genres; every genre in the dataset is a subset of one of the genres
#in this list
Genres = ['pop', 'hip hop', 'edm', 'electro', 'soul', 'r&b', 'reggae', 'dance', 'trap', 'tropical',
          'rap', 'rock', 'girl group', 'latin', 'southern', 'uk', 'australian', 'emo', 'sad',
          'k-pop', 'funk', 'boy band', 'atl', 'post-teen', 'viral', 'canadian']

@dataclass
class Song:
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


def string_to_list(string: str) -> list[str]:
    """
    This converts the string to a list of strings for Artist_Genres
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


def read_csv(filename: str) -> list[Song]:
    """
    Open the csv file in the form of a list of Songs (as in the dataclass)
    """
    input_so_far = []
    with open(filename) as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        for row in reader:
            input_so_far.append(Song(int(row[0]), row[1], row[2], int(row[3]), row[4], row[5],
                                     row[6], int(row[7]), row[8], int(row[9]), int(row[10]),
                                     string_to_list(row[11])))

    return input_so_far


def categorise_by_year(lst_total: list[Song]) -> list[list[Song]]:
    """
    Categorises the entire list of Songs by year
    """
    lsts_by_year = []
    for i in range(5):
        lsts_by_year.append([])

    for i in range(5):
        for each_song in lst_total:
            if str(i+2017) in each_song.Week:
                lsts_by_year[i].append(each_song)

    return lsts_by_year


def categorise_by_genre(lst: list[Song]) -> list[tuple[dict[str, int], list[Song]]]:
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
        tup2 = []          # 2nd element of the tuple

        for each_song in lst:
            if genre in str(each_song.Artist_Genres):
                tup2.append(each_song)

        tup1[genre] = len(tup2)

        # A way around the lack of an index; for each genre, its corresponding information is
        # mapped to the same index the genre has in the list Genres, creating parallelism between
        # the lists
        final_lst[Genres.index(genre)].append(tup1)
        final_lst[Genres.index(genre)].append(tup2)

    for i in range(len(Genres)):
        final_lst[i] = tuple(final_lst[i])

    return final_lst

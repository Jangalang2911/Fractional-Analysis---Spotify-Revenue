"""
File read the spotify revenue csv file
"""
import csv
import statistics


def read_csv(str1: str, str2: str, str3: str) -> dict[str: (int, int, int)]:
    """
    Read the revenue, users, and subscription csv files
    """
    dict1 = {}
    with open(str1) as file:
        reader = csv.reader(file, delimiter=',')
        for _ in range(5):
            next(reader)
        for row in reader:
            dict1[row[0]] = int(row[1])
    dict2 = {}
    with open(str2) as file:
        reader = csv.reader(file, delimiter=',')
        for _ in range(9):
            next(reader)
        for row in reader:
            dict2[row[0]] = int(row[1])
    dict3 = {}
    with open(str3) as file:
        reader = csv.reader(file, delimiter=',')
        for _ in range(9):
            next(reader)
        for row in reader:
            dict3[row[0]] = int(row[1])
    l1 = [dict1[items] for items in dict1]
    l2 = [dict2[items] for items in dict2]
    l3 = [dict3[items] for items in dict3]
    dict4 = {}
    for item in dict1:
        for i in range(len(l1)):
            if dict1[item] == l1[i]:
                dict4[item] = (l1[i], l2[i], l3[i])
    return dict4


def find_rsquare(dict1: dict[str: (int, int, int)]) -> list[tuple[float, float], tuple[float, float]]:
    """
    Find R for the spotify_revenue file
    """
    list_of_items = [dict1[item] for item in dict1]
    lp1 = []
    lp2 = []
    lr = []
    for item in list_of_items:
        lp1.append(item[1])
        lp2.append(item[2])
        lr.append(item[0])
    avg_x1 = statistics.mean(lp1)
    avg_x2 = statistics.mean(lp2)
    avg_y = statistics.mean(lr)
    n1 = 0
    n2 = 0
    n3 = 0
    d11 = 0
    d21 = 0
    d31 = 0
    d12 = 0
    d22 = 0
    d32 = 0
    for i in range(len(lp1)):
        n1 = n1 + (lp1[i] - avg_x1) * (lr[i] - avg_y)
        n2 = n2 + (lp2[i] - avg_x2) * (lr[i] - avg_y)
        n3 = n3 + (lp2[i] - avg_x2) * (lp1[i] - avg_x1)
        d11 = d11 + (lp1[i] - avg_x1) ** 2
        d21 = d21 + (lr[i] - avg_y) ** 2
        d31 = d31 + (lp2[i] - avg_x2) ** 2
        d12 = d12 + (lr[i] - avg_y) ** 2
        d22 = d22 + (lr[i] - avg_y) ** 2
        d32 = d32 + (lp1[i] - avg_x1) ** 2

    r1 = n1/((d11 * d12)**0.5)
    r2 = n2/((d21 * d22)**0.5)
    r3 = n3/((d31 * d32)**0.5)

    r1 = r1 ** 2
    r2 = r2 ** 2
    r3 = r3 ** 2

    return [(r1, 0), (r2, r3)]

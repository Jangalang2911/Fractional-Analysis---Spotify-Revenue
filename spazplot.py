"""
Plotting shit
"""
from sklearn.model_selection import train_test_split
import file_2 as f2
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split


dict1 = f2.read_csv('spotify_revenue.csv', 'Normal users spotify.csv',
                    'premium subscribers spotify.csv')
lst_of_coords = [dict1[item] for item in dict1]
df = pd.DataFrame(lst_of_coords)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for tup in lst_of_coords:
    ax.scatter(tup)

ls1 = [i[0] for i in lst_of_coords]
ls2 = [i[1] for i in lst_of_coords]
ls3 = [i[2] for i in lst_of_coords]




plt.show()

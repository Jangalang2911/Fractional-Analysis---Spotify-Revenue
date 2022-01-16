import matplotlib.pyplot as plt
import numpy as np
import file_2 as f2
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import datasets, linear_model


# Reading in the data from the dataset in the form of tuples
dict1 = f2.read_csv('spotify_revenue.csv', 'Normal users spotify.csv',
                    'premium subscribers spotify.csv')
lst_of_coords = [dict1[item] for item in dict1]

# Setting up the 3-dimensional space
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# Charting the plots from the dataset in the given space
for tup in lst_of_coords:
    ax.scatter(tup[2], tup[1], tup[0])
# Here, tup[2] represents revenue, tup[1] represents the number of premium subscribers, and
# tup[0] represents the number of ad-supported subscribers

# plane of best fit
df = pd.DataFrame(lst_of_coords)  # converting the list of coordinates to a numpy dataframe

target = df[0].copy()  # extracting the revenue column from the dataframe
predictors = df.drop(columns=[0]) # using the remaining dataframe as the predictors

x_train, x_test, y_train, y_test = train_test_split(predictors, target, test_size=1, random_state=1)
# Since we are not seeking to assess the prediction accuracy of the linear model, we've set the
# test_size to 1


lm = linear_model.LinearRegression()
lm.fit(x_train, y_train)
z_values = lm.predict(predictors)

# z_values contains the predicted values of the revenue from the linear model fitted using sklearn.
# We chose three random points from the data and replaced the actual revenue values with the
# predicted revenue values; these points were then utilized to graph the plot of best fit; the
# vector product for these three points was used to find the normal to the plane
points = [[52, 83, z_values.tolist()[0]],
          [83, 101, z_values.tolist()[5]],
          [100, 123, z_values.tolist()[8]]]

p0, p1, p2 = points
x0, y0, z0 = p0
x1, y1, z1 = p1
x2, y2, z2 = p2

ux, uy, uz = u = [x1 - x0, y1 - y0, z1 - z0]
vx, vy, vz = v = [x2 - x0, y2 - y0, z2 - z0]

u_cross_v = [uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx]

point = np.array(p0)
normal = np.array(u_cross_v)

d = -point.dot(normal)

xx, yy = np.meshgrid(range(200), range(250))

z = (-normal[0] * xx - normal[1] * yy - d) * 1. / normal[2]
ax.plot_surface(xx, yy, z, alpha=0.2)

plt.show()

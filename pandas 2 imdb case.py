# importing libraries
import pandas as pd
import numpy as np

# _________________________________________________________________________________________________ #

# setting PD output width and column number
desired_width = 300
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 120)
pd.set_option("display.max_rows",500)

# _________________________________________________________________________________________________ #

# # changing index, taking unnamed as the index
movies = pd.read_csv("movies.csv", index_col=0)
print(movies)
directors = pd.read_csv("directors.csv", index_col=0)
print(directors.head())

# _________________________________________________________________________________________________ #

#checking if directors in movie and director is same.
print(np.all(movies["director_id"].isin(directors["id"])))

# _________________________________________________________________________________________________ #

# joining movies(left) and directors(right) -- left outer join
md = movies.merge(directors, how="left", left_on="director_id", right_on="id")
md.drop(["id_y"], axis=1, inplace=True)
print(md.head(10))
print(md.info())

# _________________________________________________________________________________________________ #

# converting revenue and budget in millions
md["revenue"] = md["revenue"] / 1000000
md["budget"] = md["budget"] / 1000000
print(md['revenue'])
print(md['budget'])

# _________________________________________________________________________________________________ #

# # querying dataframe to fetch the data

# top voted movie #
print(md.loc[md['vote_average'] >= 8, ['title', "vote_average"]])

# avg rating greater than 7 and year 2015 or higher #
print(md.loc[(md['vote_average'] >= 7) & (md['year'] >=2015)].head())
 
# _________________________________________________________________________________________________ #

# # String methods - startwith, contain

# movie with Batman in the name
print(md.loc[md["title"].str.contains("Batman")])
# move starting with THE
print(md[md["title"].str.startswith("The")])
# most popular movie
print(md.sort_values("popularity", ascending= False).head(1))

# _________________________________________________________________________________________________ #
# finding the highest budget movie of every director
print(md.groupby("director_name")["budget"].max().head())
# number of movies by a director
print(md.groupby("director_name")["title"].count().head())

# _________________________________________________________________________________________________ #
# which director is the most productive director( by average movies per year)
md_agg = md.groupby("director_name")[["year", "title"]].aggregate(
    {
        "year": ['min','max'],
        'title': 'count'
    }
)


md_agg.columns = ["_".join(col) for col in md_agg.columns]
md_agg = md_agg.reset_index()
md_agg['active year'] = md_agg['year_max']-md_agg['year_min']
md_agg['movies per year'] = md_agg['title_count']/md_agg['active year']
print(md_agg.sort_values("movies per year", ascending= False))

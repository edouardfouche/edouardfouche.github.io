---
layout: post
title:  "arXiv and the Information Explosion"
date:   2020-11-18 08:00:00 +0100
comments: true
categories: Machine Learning
---

Nowadays, it has become more and more common to publish on [arXiv][arXiv] before peer-review. There are several (good) reasons for that: (1) Academic publishing takes too much time, and even then, (2) your paper often ends up behind a paywall. In over-hyped fields, the state of the art may change every month (or sometimes, week!), so it is a good way to "plant the flag" on your research idea. But what are the consequences of that? 

This indeed comes with some drawbacks. Before it was "cool" to publish on [arXiv][arXiv], researchers had no other option but to publish in peer-reviewed journals or conferences, which only have room for a few hundreds of papers per year. As of 2020, we are now facing more than 44K paper per year being published on [arXiv][arXiv], just for the field of Computer Science! This more than 155K per year, all categories together.

Even if scientists tend to specialize in small niches, it becomes challenging to stay up to date with the progress in your field. If you were to read, say 1K new paper per year, that would be about 3 per day -- and you also need to allocate time to *your* research. As a researcher, it just becomes harder and harder to decide what to read. 

So, will the number of submissions per year continue to increase? Let's find out. 

Mining the [arXiv][arXiv] Metadata
==================================

You can reproduce everything here from this GitHub [repository][github]. [arXiv][arXiv] does publish some statistics. For example, [here][arXivstats]. However, the plots are somewhat clunky. We obtained the MetaData about every paper submitted on [arXiv][arXiv] from [here][arXivdata]. 

Preparing the data
------------------

Let's open a Jupyter notebook, import some package and define some style. 

```python
import math
import json 
import copy
from datetime import datetime

import pandas as pd
import numpy as np
from scipy import interpolate

import matplotlib as mpl
from matplotlib import cm
import matplotlib.ticker as mtick
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rc
```

```python
# Some styling 
mpl.rcParams['text.usetex'] = True 
mpl.rcParams['text.latex.preamble'] = r'\usepackage{libertine}' 
mpl.rc('font', family='serif')
mpl.rcParams['ps.usedistiller'] = 'xpdf' 
plt.style.use('seaborn-notebook')
plt.rcParams['axes.titlesize'] = '25'
plt.rcParams['axes.labelsize'] = '25'
plt.rcParams['legend.fontsize'] = '15'
plt.rcParams['xtick.labelsize'] = '15'
plt.rcParams['ytick.labelsize'] = '15'

# Some colors
uiucblue = (19/255,42/255,76/255)
uiucred = (232/255,74/255,39/255)
kitgreen = (50/255,161/255,137/255)
```

We need to parse the JSON file (download from [here][arXivdata]). It may be tempting to do something like this:

```python
pd.read_json('arxiv-metadata-oai-snapshot.json', lines=True)
```

This will likely lead to a memory error, as you are reading a 2.9GB JSON file. 

It is better to parse this JSON file the "old school" way: 

```python
f = open('arxiv-metadata-oai-snapshot.json')

i = 0
ignores = ['abstract', 'authors_parsed', 'versions']  # let's ignore those fields
record = f.readline()
results = []

while (record !=  ''): # do this until file is empty
    res = json.loads(record) 
        
    version = res["versions"][0] # take only the first version
    res['version'] = version['version']
    res['created'] = version['created']
    
    for ignore in ignores: # save space
        del res[ignore]
    results.append(res)
    
    record = f.readline()  # go for the next record 
    i += 1

data = pd.DataFrame(results)
```

We keep each record in a `list` and then create a `DataFrame` (it is much fast than appending the DataFrame over and over). We now have a `DataFrame` with around 1.7M records! 

Let's now extract the main category for each paper and the year of creation. 

```python
data['maincat'] = [x.split(" ")[0].split(".")[0] for x in data["categories"]] 
data["date"] = pd.to_datetime(data["created"]) # this takes some time
data['year'] = pd.DatetimeIndex(data['date']).year 
```

We can see that there are 38 categories and also some papers created before `1991`, the year [arXiv][arXiv] was created. Let's clean that up! 

```python
data["maincat"] = data["maincat"].replace("hep-ex", "hep-*")
data["maincat"] = data["maincat"].replace("hep-lat", "hep-*")
data["maincat"] = data["maincat"].replace("hep-ph", "hep-*")
data["maincat"] = data["maincat"].replace("hep-th", "hep-*")

data["maincat"] = data["maincat"].replace("math-ph", "math")
data["maincat"] = data["maincat"].replace("nucl-th", "nucl")
data["maincat"] = data["maincat"].replace("q-fin", "q-fin+econ")
data["maincat"] = data["maincat"].replace("econ", "q-fin+econ")

data["maincat"] = data["maincat"].replace("physics", "physics+gr-qc+nlin+nucl+quant-ph")
data["maincat"] = data["maincat"].replace("gr-qc", "physics+gr-qc+nlin+nucl+quant-ph")
data["maincat"] = data["maincat"].replace("nlin", "physics+gr-qc+nlin+nucl+quant-ph")
data["maincat"] = data["maincat"].replace("nucl", "physics+gr-qc+nlin+nucl+quant-ph")
data["maincat"] = data["maincat"].replace("quant-ph", "physics+gr-qc+nlin+nucl+quant-ph")
```

```python
# Year 2020 is not over yet, so let's discard it, arXiv started in 1991
toplot = data[(data["year"] >= 1991) & (data["year"] <= 2019)]

# Get the cumulative counts for each main category per year
cumulative = toplot.groupby(["year", "maincat"])[["id"]].count().reset_index().pivot_table(
    index=["year"], columns=["maincat"]).fillna(0).cumsum()

# Get the max for each category
maxcounts = cumulative.max().reset_index()[["maincat", 0]].set_index("maincat")

# Some formatting
cumulative.columns =  cumulative.columns.droplevel(0)
cumulative.columns.name = None

# Let's keep the categories with more than 10000 papers 
tokeep = maxcounts[maxcounts[0] > 10000].sort_values(0).index
```

So we now have the cumulative counts for each main category. As we can see, there were more than 155K submissions in 2019!

```python
cumulative.T.sum()[2019] - cumulative.T.sum()[2018] # -> 155917
```

Visualize
---------

```python
%matplotlib notebook

cumulative[tokeep].plot.area(cmap="coolwarm")
plt.title("Number of articles on arXiv per category")
plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))
plt.xticks([1991+x for x in range(2019-1991+1)], 
           [1991+x  if x%4==0 else "" for x in range(2019-1991+1)])
handles, labels = plt.gca().get_legend_handles_labels()
plt.gca().legend(handles[::-1], labels[::-1], frameon=False)
plt.xlabel("") 
```

![counts_arxiv](/img/arxiv-information-explosion/counts_arxiv.svg){:class="img-responsive"}

Warmer colours are for categories with more submissions (in 2019). As we can see, Computer Science (cs) only recently become a major field on [arXiv][arXiv], but it is increasing fast! Let's have a look at the relative counts: 

```python
relative = copy.deepcopy(cumulative[tokeep])
yearsum = cumulative[tokeep].T.sum()
relativeT = relative.T
for col in relativeT.columns:
    relativeT[col] = relativeT[col] / yearsum[col]
relative = relativeT.T

%matplotlib notebook

ax = relative[tokeep].plot.area(cmap="coolwarm")
plt.tight_layout()
plt.title("Relative number of articles on arXiv")
plt.gca().yaxis.set_major_formatter(mtick.ScalarFormatter())
plt.xticks([1991+x for x in range(2019-1991+1)], 
           [1991+x  if x%4==0 else "" for x in range(2019-1991+1)])
plt.gca().get_legend().remove()
plt.xlabel("")
plt.ylim(0,1)

plt.gca().text(2015, 0.87, "math", fontsize=15)
plt.gca().text(2014, 0.68, "physics+...", fontsize=15)
plt.gca().text(2014, 0.50, "cond-math", fontsize=15)
plt.gca().text(2014.5, 0.35, "astro-ph", fontsize=15)
plt.gca().text(2015, 0.20, "hep-*", fontsize=15)
plt.gca().text(2017, 0.07, "cs", fontsize=15)
```

![relative_counts_arxiv](/img/arxiv-information-explosion/relative_counts_arxiv.svg){:class="img-responsive"}

So the category `hep-*` (High Energy Physics), has been most prominent for a long time, now it is `math` and `physics`. Let's see how fast the total number of paper (the size of the [arXiv][arXiv]!) has evolved over time:

```python
y = np.array(cumulative.T.sum())

ref = pd.Series([val for val in y])
ref.index = cumulative[tokeep].T.sum().index
plt.plot(ref, color=uiucblue, linewidth=5)

ax = plt.gca()
ax.set_yscale('log', basey=2)
plt.yticks([2**x for x in range(22)])
plt.xticks([1991+x for x in range(2019-1991+1)], 
           [1991+x  if x%4==0 else "" for x in range(2019-1991+1)])
plt.title("Total number of articles on arXiv")

f = interpolate.interp1d(y, ref.index)
for x in range(10,21):
    plt.vlines(f(2**x), 0.5, 5*10**6, alpha=0.5)
    
plt.ylim((1.1*2**8,2**22))
plt.xlim((1990, 2020))
plt.grid(linestyle="--")
```

![total_counts_arxiv](/img/arxiv-information-explosion/total_counts_arxiv.svg){:class="img-responsive"}

As we can see, the number of articles has doubled twice in 1992, then doubled every 1-2 years, and now every 5-6 years. Can we guess how many papers will be on [arXiv][arXiv] in 2030? Let's plot the evolution of the number of submission per year. 

```python
%matplotlib notebook

sums = cumulative.T.sum()
diffs = copy.deepcopy(sums)
diffs = diffs.sort_index()
for x in range(1992, 2020): # get the number of new submission per year
    diffs[x] = diffs[x] - sums[x-1]
plt.bar(diffs.index, diffs, color=uiucblue)

x = np.array(diffs.index)
y = np.array(diffs)

# Let's fit a second-order polynomial 
z = np.polyfit(x, y, 2, full=True)
fit2 = np.poly1d(z[0])
fitted = pd.Series([fit2(val) for val in list(x) + [2020 + x for x in range(10)]])
fitted.index = list(diffs.index) + [2020 + x for x in range(10)]
plt.plot(fitted, color=uiucred, linestyle="--", label="second-order")

# Let's fit a third-order polynomial 
z = np.polyfit(x, y, 3, full=True)
fit3 = np.poly1d(z[0])
fitted = pd.Series([fit3(val) for val in list(x) + [2020 + x for x in range(10)]])
fitted.index = list(diffs.index) + [2020 + x for x in range(10)]
plt.plot(fitted, color=kitgreen, label="third-order")

plt.xticks([1991+x for x in range(2030-1991+1)], 
           [1991+x  if x%4==0 else "" for x in range(2030-1991+1)])
plt.legend()

plt.title("Number of submissions / year")
plt.grid(linestyle="--", axis="y")
```

![submissions_per_year_arxiv_forecast](/img/arxiv-information-explosion/submissions_per_year_arxiv_forecast.svg){:class="img-responsive"}

We have also fitted a second and third-order polynomial to the evolution of the number of submissions. The third-order polynomial fits the bars quite nicely but leads to a steep increase. In comparison, the second-order polynomial feels more realistic. 

With the second-order polynomial, we can forecast that there will be about 3.6M papers on [arXiv][arXiv], while the third-order polynomial expects about 4.1M.  

```python
# Expected total number of submission by 2030
int(diffs.sum() + sum([fit2(2020 + x) for x in range(10)])) # -> 3619959
int(diffs.sum() + sum([fit3(2020 + x) for x in range(10)])) # -> 4087884
```

Who is right? Only time will tell. It depends on how many scientists in the world are there, who do not *yet* use [arXiv][arXiv] —Rendez-vous in 2030. 

And what about Computer Science?
--------------------------------

As we could see, the number of submissions has increased steeply in recent years. Let's have a look!

```python
data_cs = copy.deepcopy(data[data['maincat'] == "cs"])
data_cs.loc[:,'subcat'] = [x.split(" ")[0].split(".")[1] for x in data_cs["categories"]]
toplot = data_cs[(data_cs["year"] >= 1991) & (data_cs["year"] <= 2019)]
cumulative = toplot.groupby(["year", "subcat"])[["id"]].count().reset_index().pivot_table(
    index=["year"], columns=["subcat"]).fillna(0).cumsum()
cumulative.columns =  cumulative.columns.droplevel(0)
cumulative.columns.name = None
cumulative.T.sum()[2019] - cumulative.T.sum()[2018] # 43939 new submission in 2019
tokeep = cumulative.max().sort_values(0).index # sort by decreasing

cumulative[tokeep].plot.area(cmap="coolwarm")
plt.title("Number of CS articles on arXiv")
plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))
plt.xticks([1991+x for x in range(2019-1991+1)], 
           [1991+x  if x%4==0 else "" for x in range(2019-1991+1)])
handles, labels = plt.gca().get_legend_handles_labels()
plt.gca().legend(handles[::-1], labels[::-1], ncol=3, frameon=False)
plt.xlabel("")
```

![counts_arxiv_cs](/img/arxiv-information-explosion/counts_arxiv_cs.svg){:class="img-responsive"}

That is a much faster increase as before! What about the relative counts?

```python
relative = copy.deepcopy(cumulative)
yearsum = cumulative.T.sum()
relativeT = relative.T
for col in relativeT.columns:
    relativeT[col] = relativeT[col] / yearsum[col]
relative = relativeT.T

ax = relative[tokeep].plot.area(cmap="coolwarm")
relative[tokeep].plot(stacked=True, color="black", alpha=0.8, ax=ax, linewidth=0.5)
plt.title("Relative number of CS articles on arXiv")
plt.gca().yaxis.set_major_formatter(mtick.ScalarFormatter())
plt.xticks([1991+x for x in range(2019-1991+1)], 
           [1991+x  if x%4==0 else "" for x in range(2019-1991+1)])
plt.gca().get_legend().remove()
plt.xlabel("")
plt.ylim(0,1)
```
![relative_counts_arxiv_cs](/img/arxiv-information-explosion/relative_counts_arxiv_cs.svg){:class="img-responsive"}

So at the very start, there were only three categories: `DS` (Data Structures and Algorithms), `CC` (Computational Complexity), and `GL` (General Literature). In the early 90s, the `AI` (Artificial Intelligence) community massively submitted to [arXiv][arXiv], but the larger fields are now `CV` (Computer Vision), `IT` (Information Theory), `LG` (Machine Learning), and `CL` (Computation and Language). 

As an exercise for you: How many computer science articles will we have on [arXiv][arXiv] in 2030? Of course, you can use the polynomial-fitting technique above, but the question is instead: How many more paper per year will the community post on [arXiv][arXiv]?

Threats and Opportunities
=========================

As we have more and more papers, each of them gets less and less exposure (unless if you work with someone famous?). In the end, one may only consider those with more citations. But getting citations is a tricky business (more on that later, probably). Although citations are often being used as a proxy for quality, they do not help us to find new problems, i.e., those which did not get much attention so far! 

In the future, it may become more likely that we will reinvent things over and over again, simply because they have gone unnoticed. By systemically exploring the papers being published (via Data Mining, Machine Learning, etc.), can we find new trends? New subfields? 

The massive information explosion on [arXiv][arXiv] also opens the ways to exciting research directions. [arXiv][arXiv] can be a great tool to explore the historical evolution of a particular field. For this, however, you might need to dive deeper into the semantics of the papers. Luckily we now have many great tools to extract semantic information from text! Interesting questions are, for example: 

- What has been the focus of community `X` over the past few years? How did it change? 
- What are the common interests between community `X` and `Y`? How much do they overlap? 
- Can one see community `X` and a parent of community `Y`? 

Getting answers to such questions may be not only interesting from a historical perspective but also to identify new trends and emerging fields! Finally, it would be nice to visualize the relationship between communities at different points in time and create better taxonomies.

[arXiv]: https://arxiv.org/
[arXivstats]: https://arxiv.org/help/stats/2019_by_area/index
[arXivdata]: https://www.kaggle.com/Cornell-University/arxiv/tasks
[pdf2svg]: https://github.com/dawbarton/pdf2svg
[github]: https://github.com/edouardfouche/arxiv-information-explosion
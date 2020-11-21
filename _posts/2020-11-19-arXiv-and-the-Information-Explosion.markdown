---
layout: post
title:  "arXiv and the Information Explosion"
date:   2020-11-18 08:00:00 +0100
comments: true
categories: Machine Learning
---

Nowadays, it has become more and more common to publish on [arXiv][arXiv] before peer-review. There are several (good) reasons for that: (1) Academic publishing takes too much time, and even then, (2) your paper often ends up behind a paywall. In over-hyped fields, the state of the art may change every month (or sometimes, week!), so it is a good way to "plant the flag" on your research idea. But what are the consequences of that? 

This indeed comes with some drawbacks. Before it was "cool" to publish on [arXiv][arXiv], researchers had no other option but to publish in peer-reviewed journals or conferences, which only have room for a few hundreds of papers per year. As of 2020, we are now facing more than 44K paper per year being published on [arXiv][arXiv], just for the field of Computer Science! This more than 155K per year, all categories together.

Even if scientists tend to specialize in small niches, it becomes challenging to stay up to date with the progress in your field. If you were to read, say 1K new paper per year, that would be about 3 per day -- and you also need to allocate time to *your* research. As a researcher, it just becomes harder and harder to decide what to read. So, will the number of submissions per year continue to increase? Let's find out. 

Mining the [arXiv][arXiv] Metadata
==================================

You can reproduce all the plots from this GitHub [repository][github]. Note that [arXiv][arXiv] does publish some statistics. For example, [here][arXivstats]. However, the plots are somewhat clunky. We obtained the MetaData about every paper submitted on [arXiv][arXiv] from [here][arXivdata]. 

![counts_arxiv](/img/arxiv-information-explosion/counts_arxiv.svg){:class="img-responsive"}

Warmer colours are for categories with more submissions (in 2019). As we can see, Computer Science (cs) only recently become a major field on [arXiv][arXiv], but it is increasing fast! Let's have a look at the relative counts: 

![relative_counts_arxiv](/img/arxiv-information-explosion/relative_counts_arxiv.svg){:class="img-responsive"}

So the category `hep-*` (High Energy Physics), has been most prominent for a long time, now it is `math` and `physics`. Let's see how fast the total number of paper (the size of the [arXiv][arXiv]!) has evolved over time:

![total_counts_arxiv](/img/arxiv-information-explosion/total_counts_arxiv.svg){:class="img-responsive"}

As we can see, the number of articles has doubled twice in 1992, then doubled every 1-2 years, and now every 5-6 years. Can we guess how many papers will be on [arXiv][arXiv] in 2030? Let's plot the evolution of the number of submission per year. 

![submissions_per_year_arxiv_forecast](/img/arxiv-information-explosion/submissions_per_year_arxiv_forecast.svg){:class="img-responsive"}

We have also fitted a second- and third-order polynomial to the evolution of the number of submissions. The third-order polynomial fits the bars quite nicely but leads to a steep increase. In comparison, the second-order polynomial feels more realistic. With the second-order polynomial, we forecast that there will be about 3.6M papers on [arXiv][arXiv] in 2030, while the third-order polynomial expects about 4.1M.  

Who is right? Only time will tell. It depends on how many scientists in the world are there, who do not *yet* use [arXiv][arXiv] —Rendez-vous in 2030. 

And what about Computer Science?
--------------------------------

As we could see, the number of submissions has increased steeply in recent years. Let's have a look!

![counts_arxiv_cs](/img/arxiv-information-explosion/counts_arxiv_cs.svg){:class="img-responsive"}

That is a much faster increase as before! What about the relative counts?

![relative_counts_arxiv_cs](/img/arxiv-information-explosion/relative_counts_arxiv_cs.svg){:class="img-responsive"}

So at the very start, there were only three categories: `DS` (Data Structures and Algorithms), `CC` (Computational Complexity), and `GL` (General Literature). In the early 90s, the `AI` (Artificial Intelligence) community massively submitted to [arXiv][arXiv], but the larger fields are now `CV` (Computer Vision), `IT` (Information Theory), `LG` (Machine Learning), and `CL` (Computation and Language). 

As an exercise for you: How many computer science articles will we have on [arXiv][arXiv] in 2030? Of course, you can use the polynomial-fitting technique above, but the question is instead: How many more paper per year will the community post on [arXiv][arXiv]?

Threats and Opportunities
=========================

As we have more and more papers, each of them gets less and less exposure (unless if you work with someone famous?). In the end, one may only consider those with more citations. But getting citations is a tricky business (more on that later, probably). Although citations are often being used as a proxy for quality, they do not help us to find new problems, i.e., those which did not get much attention so far! 

In the future, it may become more likely that we will reinvent things over and over again, simply because they have gone unnoticed. By systemically exploring the papers being published (via Data Mining, Machine Learning, etc.), can we find new trends? New subfields? 

The massive information explosion on [arXiv][arXiv] opens the ways to exciting research directions. [arXiv][arXiv] can be a great tool to explore the historical evolution of a particular field. For this, however, you might need to dive deeper into the semantics of the papers. Luckily we now have many great tools to extract semantic information from text! Interesting questions are, for example: 

- What has been the focus of community `X` over the past few years? How did it change? 
- What are the common interests between community `X` and `Y`? How much do they overlap? 
- Can one see community `X` and a parent of community `Y`? 

Getting answers to such questions may be not only interesting from a historical perspective but also to identify new trends and emerging fields! Finally, it would be nice to visualize the relationship between communities at different points in time and create better taxonomies.

[arXiv]: https://arxiv.org/
[arXivstats]: https://arxiv.org/help/stats/2019_by_area/index
[arXivdata]: https://www.kaggle.com/Cornell-University/arxiv/tasks
[pdf2svg]: https://github.com/dawbarton/pdf2svg
[github]: https://github.com/edouardfouche/arxiv-information-explosion
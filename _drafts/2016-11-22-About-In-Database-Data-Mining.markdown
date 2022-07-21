---
layout: post
title:  "About In-Database Data Mining"
date:   2016-11-22 11:31:00 +0100
comments: true
categories: other
---

Current approaches in Data Mining and Machine Learning require the data to be first extracted from an underlying database. From a practical point of view, this has many drawbacks. In this article, I will discuss to what extend we could take advantage of database systems to conduct data analysis.

Databases are everywhere, but they are limited
----------------------------------------------

Databases are the backbone of any multi-tier architecture. They are very mature and provide a reliable way to store, organize and retrieve data. Nowadays, Data Warehouses are an important (if not the most important) artifact of business intelligence systems. They provide a starting point and universal data source for creating analytics reports to support business decisions. 

However, they are limited. If one wants to perform advanced data analytics, such as predicting customer churn or forecasting future profits, the data needs to be extracted first. Database systems generally do not offer advanced analytics features. There are a few reasons:
- There is a wide-range of database systems and they handle data quite differently, so creating different implementations of the same algorithms to accommodate different back-ends is a loss of time.  
- Many well-established database systems are proprietary, excluding open-source contributions.  
- There is a tremendous amount of data mining algorithms, serving different purposes, such that one can only map a small subset of the existing algorithms. 
- The focus of database development is set on efficient storage and retrieval of data, not its analysis.

As a consequence, most machine learning applications read data from system-agnostic data formats, such as txt or csv files. 

Extracting data is problematic
------------------------------

The need for extracting this data from database systems brings several major drawbacks: 

- If the data is big, it is impractical or impossible to download it. 
- If the data volume exceeds the RAM limit of the target machine, analysis becomes challenging.
- When the data changes, duplicates need be refreshed, requiring expensive synchronisation episodes. 
- It creates important security concerns: If the data is sensitive, the flow of extracted data needs to be encrypted, as well as the duplicates of the data stored in the hard-drive. This is especially critical if the data contains information such as tactical business indicators or customer-related attributes (e.g. credit card numbers). Also, data duplicates create vunerability breaches for a business. 

A possible solution: SQL-Pushdowns
----------------------------------

The ''SQL-Pushdown'' approach simply consists in mapping high-level syntax into SQL code and push it to the database for execution. This approach is advantageous, because it is exactly as powerful as querying the database using SQL, without the burden of writing SQL. 

Let me give you an example: Let's compute the mean for each attribute grouped by class in the IRIS dataset. IRIS is a standard toy dataset in machine learning. Ronald Fisher used it to illustrate the effect of the discriminant that bears his name. It looks like this: 

| Sepal_Length  | Sepal_Width | Petal_Length | Petal_Width  | Species  |
|---|---|---|---|---|
| 5.1  |  3.5 | 1.4  | 0.2  | setosa  |
| 4.9  | 3.0  | 1.4  | 0.2  | setosa  |
|  4.7 | 3.2  | 1.3  | 0.2  | setosa  |
|  4.6 | 3.1  | 1.5  | 0.2  | setosa  |
|  5.0 | 3.6  | 1.4  | 0.2  | setosa  |

And we are expecting this table as a result, where the values are the means for each class: 

|  | Sepal_Length  | Sepal_Width | Petal_Length | Petal_Width  |
|---|---|---|---|---|
| **setosa**  | 5.006 | 3.428  | 1.462  | 0.246  |
| **versicolor**  | 5.936  | 2.770  | 4.260  | 1.326  |
|  **virginica** | 6.588  | 2.974  | 5.552  | 2.026  |

In SQL, we would need to issue the following query: 

{% highlight SQL %}
SELECT AVG(Sepal_Length), AVG(Sepal_Width), AVG(Petal_Length), AVG(Petal_Width) 
FROM IRIS 
GROUP BY Species
{% endhighlight %}

In Python or R, we could do it with a single command: 

- Python
{% highlight Python %}
iris.groupby('Species').mean()
{% endhighlight %}

- R
{% highlight R %}
aggregate(.~Species, iris, mean)
{% endhighlight %}

SQL is not a complicated language. But if the names of the columns change or if we add more columns, SQL queries need to be rewritten. This example is simple, but if we use SQL to conduct more advanced analytics, it becomes difficult to manage, because SQL is too low level. So the idea is to have some kind of interface, which translate high-level syntax into SQL. 

[comment]: There is a Python package called `ibmdbpy`. It is open-source, pip-installable and available here. Ibmdbpy connects to an IBM DB2 or IBM dashDB database, and translates Pandas-like syntax into SQL, that gets pushed to the database. The result is mapped back in a Python data structure such as a `pandas.DataFrame` object. 

In-Database correlation computation
-----------------------------------

During my master thesis, I have been investigating how to map the computation of various correlation coefficients to database systems, using the SQL-Pushdown approach. Pairwise correlation coefficients between attributes are interesting in many scenarios, such as feature selection. Based on correlation, it is possible to identify interesting patterns, or a subset of attributes that are best suited for making a prediction. Furthermore, the use of the SQL-Pushdown approach provides several advantages:

- We do not need to extract the data from database (avoiding the associated problems).
- We take advantage of database specific features, such as columnar technology and index structures.
- We take advantage of the database hardware, typically better than commodity hardware.
- It is certain that we are using the most recent version of the data.

For example, if we want to compute the mutual information for each attribute against the class in the iris data set, the following SQL-Pushdown operation can be used: 

{% highlight Python %}
>>> info_gain(iris, target="CLASS")
> SELECT CAST(COUNT(*) AS INTEGER) FROM DB2INST1.IRIS
> SELECT SUM(-a*LOG(a)) FROM(SELECT COUNT(*) AS a FROM DB2INST1.IRIS GROUP BY "CLASS")
> SELECT SUM(-a*LOG(a)) FROM(SELECT COUNT(*) AS a FROM DB2INST1.IRIS GROUP BY "SEPALLENGTH")
> SELECT SUM(-a*LOG(a)) FROM(SELECT COUNT(*) AS a FROM DB2INST1.IRIS GROUP BY "CLASS","SEPALLENGTH")
> SELECT SUM(-a*LOG(a)) FROM(SELECT COUNT(*) AS a FROM DB2INST1.IRIS GROUP BY "SEPALWIDTH")
> SELECT SUM(-a*LOG(a)) FROM(SELECT COUNT(*) AS a FROM DB2INST1.IRIS GROUP BY "CLASS","SEPALWIDTH")
> SELECT SUM(-a*LOG(a)) FROM(SELECT COUNT(*) AS a FROM DB2INST1.IRIS GROUP BY "PETALLENGTH")
> SELECT SUM(-a*LOG(a)) FROM(SELECT COUNT(*) AS a FROM DB2INST1.IRIS GROUP BY "CLASS","PETALLENGTH")
> SELECT SUM(-a*LOG(a)) FROM(SELECT COUNT(*) AS a FROM DB2INST1.IRIS GROUP BY "PETALWIDTH")
> SELECT SUM(-a*LOG(a)) FROM(SELECT COUNT(*) AS a FROM DB2INST1.IRIS GROUP BY "CLASS","PETALWIDTH")

PETALLENGTH    1.446317
PETALWIDTH     1.435898
SEPALLENGTH    0.876938
SEPALWIDTH     0.510870
Name: CLASS, dtype: float64
{% endhighlight %}

Note that in this case, the real-valued attributes need to be discretized in a first step.

[comment]:  mapping Feature Selection algorithms to database using this approach. Feature Selection refers to a range of method, which are used to select a subset of attributes in order to optimize the performance of underlying machine learning algorithms. The idea is to keep the most relevant features and discard useless features. This brings several advantages, such as a reduction of the required training time, better performance and avoidance of overfitting. 

[comment]: There are mainy ways to conduct Feature Selection, but we are not going to focus on this topic in this article. However, it turns out that we can use the SQL-Pushdown approach to compute efficiently various correlation measures. Those correlation coefficients can be used in a second step for other tasks, such as Feature Selection. 

[comment]: I would like to give you an example: 




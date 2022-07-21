---
layout: post
title:  "The wonderful world of Mutual Information"
date:   2016-11-22 11:31:00 +0100
comments: true
categories: other
---

Mutual Information is an incredibly powerful concept inherited from information theory. It measures the amount of information that are shared by two entities and was successfully applied in many fields. However, it can be difficult to estimate in practice. In this article, I will try to provide a comprehensive description of this concept and show how we can use it.  

Mutual Information is tied to Shannon's entropy. The entropy of a random variable give an indication about how random the distribution of its possible values is. It can be interpreted as a measure of incertainty or disorder. The entropy is defined as following: 

(S) = - sum_{j} p_{j} * log p_{j}

where p_H{j} is the relative frequency of the Klasse j in the random variable X. 

The entropy is minimal, if there is only one class j, such that p_{j} = 1. It is maximal if for all classes i and j p_{i} = p_{j}, not that the entropy in that case increases monotonically with the number of classes. When we use logarihtm base 2, the entropy value corresponds to the number of bits required to binary encode the different values of X (?).

Now let's go back to Mutual Information. Mutual Information measures the decrease in entropy of a variable X, given that we know the variable Y. Intuitively, this give an estimation how much bits of the encoding can be shared the two variables, i.e. how much information is shared. The Mutual Information can be computed this way:

I(X,Y) = H(X) - H(X/Y) 

where H(X/Y) is the so-called conditional entropy. It is equal to:

H(X/Y) = 

According to the chain rule, we can also write Mutual Information this way:

I(X,Y) = H(X) + H(Y) - H(X,Y)

where H(X,Y) is the joint entropy, i.e. the entropy of the tuple (X,Y). 

This formulation however, works only for categorical data, where we can feat each values in a particular class. There are several ways to extend the concept to numerical data. Most of them the data distribution to be extimate and discretized in some ways. Here we discuss some of these estimators: 

-
-
-
-

There exists also several approaches to extend Mutual Information outside from th bivariate case. But in that case, Mutual Information becomes difficult to interprete. 

Disregarding those practical complications, Mutual Information is an IDEAL measure to estimate the correlation between two variables. It is a non-parametric measure which, unlike Pearson's correlation, can detect non-linear dependencies. Also, it is not retricted to the monotic case like Spearman's rho correlation. 

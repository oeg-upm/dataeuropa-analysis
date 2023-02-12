# DataEuropa Analysis

Public organisations are publishing their datasets in data.europa.eu. Several studies are conducted to measure the reuse of these datasets. The aim of this repository is to understand the context in which these datasets are mentioned and analyse the reuse of these datasets from other platforms, such as StackOverflow, Reddit, and GitHub.

[//]: # (Repository for the analysis of data.europa.eu done in task 3.4)


## Outline
1. [Data Collection](#data-collection) 
2. Analysis 
3. Experimentation
4. Tests
5. Contributors


## Data Collection
In this process, the data (e.g., posts) containing the link data.europa.eu is downloaded and stored. The format is different for each platform. There is a data collection module for each platform to fetch and prepare the data for the analysis phase. 


## Analysis
The analysis phase is platform agnostic. The different data collection module will call the different analysis function. 

The analysis is composed of the following:
* **Datasets .vs Datastories.**
* **Dataset Topical Analysis.**
* **Context Topical Analysis.**
* **Context Keywords.**

There is also some additional analyses that is only feasible for certain platforms (platform-specific analysis).
* Topical analysis using tags.
* Dataset/Datastory per sub-reddit.



```
python -m datacoll.stackoverflow
```


## StackOverFlow
![](stackoverflow_tags.svg)
![](stackoverflow_datasets_cats.svg)
![](stackoverflow_cat.svg)
![](stackoverflow_keywords.svg)


```
python -m datacoll.stackoverflow
```

Because "&#39" actually refers to `'`. 

## Reddit
![](reddit_cat.svg)
![](reddit_cat_per_sub.svg)
![](reddit_class.svg) 
![](reddit_keywords.svg)
#### Dataset per EDP Category
![](reddit_datasets_cats.svg) 

### Collect the data and run the analytics for Reddit
This will collect the data from reddit as json and store them if they are not collected yet and
then runs the analytics. This will also generate the different diagrams as well.
```
python -m datacoll.reddit
```


## GitHub
### Code
![](github_code.svg)
![](github_code_class.svg)
```
python -m datacoll.github code
```

### Commits
![](github_commits.svg)
![](github_commits_class.svg)
```
python -m datacoll.github commits
```


### Repositories
![](github_repositories.svg)
![](github_repositories_class.svg)
```
python -m datacoll.github repositories
```
### Distribution of data.europe.eu resources across Github sources
![](data_europe_distribution.svg)



## Tests
To run the tests
```
python -m unittest tests
```

## MISC
To compare the results from algorithm 1 (using the `body` parameter) vs algorithm 2 (using the `q` parameter)
```
python -m misc.stackoverflow_search_algorithms
```

## Contributors
* [Ahmad Alobaid](https://github.com/ahmad88me)
* [Elvira Amador-Domínguez](https://github.com/eamadord)
* [Oscar Corcho](https://github.com/ocorcho)
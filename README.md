CIRP survey of the american freshmen conducted in 2014. Contains student's opinions
on various matters as well as information about institutions participating in a survey.

## Data

Data comes from The Cooperative Institutional Research Program (CIRP) administered
by the Higher Education Research Institute at UCLA https://www.heri.ucla.edu/monographs/TheAmericanFreshman2014.pdf

It consists of several types of information:

``
1. Information obtained from the survey of freshmen about their opinions, politics,race, wealth, social status etc in file freshmen_survey.csv
2. Information about institutions participating in the 2014 CIRP Freshman Survey in file institutions.csv
3. Estimated standard errors of percentages for comparison groups of various sizes in file standard_errors.csv
``

## Preparation

The script works with python 3. To install required modules run

```
pip install -r scripts/requirements.txt
```

Also make note that java must also be installed on the system. To get the final data, use script process.py to extract resources from the file
TheAmericanFreshman2014.pdf. The script splits the document into pages and parses tables which are then merged into three resources.

```
to get freshmen_survey.csv, institutions.csv, standard_errors.csv
scripts/process.py
```

## License

Public Domain Dedication and License (PDDL)
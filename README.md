# ro-evaluation
Evaluation tools and other resources for the CLPsych 2016 shared task.

## Format 

Files should be a tab-separated list with two columns:                           
* post (message) ID                                                         
* triage label: crisis, red, amber or green

E.g.:
```
67      green
68      crisis
76      green
```

## Validation

Call as, e.g.:
```
python3 eval.py data/sample_test.tsv
python3 eval.py incorrect-samples/wrong-label
```

## Evaluation

Call as, e.g.:
```
python3 eval.py --gold data/sample_gold.tsv data/sample_test.tsv
```

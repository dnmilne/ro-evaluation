# ro-evaluation

This script helps you validate and evaluate submissions for the CLPsych 2016 and 2017 shared tasks.

## File format

Your submission file should be a tab-separated list with two columns:
* post (message) ID                                                         
* triage label: crisis, red, amber or green

E.g.:
```
67      green
68      crisis
76      green
```

## Validation

To check the submission file is formatted correctly, run:

```
python3 eval.py path/to/submission.tsv
```

To additionally check that the file contains the correct entries for a particular shared task, run:

```
python3 eval.py path/to/submission.tsv --task=clpsych16
```

or

```
python3 eval.py path/to/submission.tsv --task=clpsych17
```


## Evaluation

If you have a copy of the gold standard (i.e. hand-labeled) test set, run:

```
python3 eval.py path/to/submission.tsv --gold path/to/gold.tsv
```

Please note that the gold standard test set is only given out after the shared task has concluded.
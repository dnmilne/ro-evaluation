#!/usr/bin/env python3

"""
Script to validate and evaluate responses for the CLPsych 2016 shared task.

Files should be a tab-separated list with two columns:
    1. post (message) ID
    2. triage label: crisis, red, amber or green

This script provides a few metrics. Official score is macro-averaged F-score.
"""

import sys, argparse

LABELS = ('crisis', 'red', 'amber', 'green')

def load_and_validate(path, constraints=set()):
    """
    Validate list of triage classifications from filename.
    Load into a list of pairs.
    """
    pairs = []
    ids_found = set()

    with open(path) as f:
        for i, line in enumerate(f):
            try:
                idx, label = line.strip().split('\t')
                if label not in LABELS:
                    print('Line {} ({}) in {} has an invalid label, aborting.'\
                            .format(i, line.strip(), path), file=sys.stderr)
                    sys.exit(2)
                if idx in ids_found:
                    print('Duplicate ID on line {} ({}) in {}, aborting.'\
                            .format(i, line.strip(), path), file=sys.stderr)
                    sys.exit(3)
                ids_found.add(idx)
                if constraints and not idx in constraints:
                    print('ID on line {} ({}) in {} is not in CLPsych16 test ids, aborting.'\
                            .format(i, line.strip(), path), file=sys.stderr)
                    sys.exit(4)
                pairs.append((idx, label))
            except ValueError:
                print('Line {} ({}) in {} does not have two columns, aborting.'\
                        .format(i, line.strip(), path), file=sys.stderr)
                sys.exit(1)
    if constraints and len(constraints) != len(ids_found):
        print('Size of test data is incorrect (is {}, should be {}), aborting.'\
                .format(len(ids_found), len(constraints)), file=sys.stderr)
        sys.exit(5)
    print('{} validates.'.format(path))
    return pairs

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('test', help='Test file to evaluate.')
    p.add_argument('--gold', help='Gold file to test against. If a gold file \
            is not provided, this script will validate the test file only.')
    p.add_argument('--clpsych16', help='Add extra validation checks \
            for CLPsych16 test data.', action='store_true')
    args = p.parse_args()

    if args.clpsych16:
        ids = set()
        with open('data/test_posts.tsv') as f:
            for line in f:
                ids.add(line.strip())
        test_pairs = load_and_validate(args.test, ids)
    else:
        test_pairs = load_and_validate(args.test)
   
    if args.gold:
        gold_pairs = load_and_validate(args.gold)
        if len(test_pairs) != len(gold_pairs):
            print('Number of test and gold instances is not equal, aborting.', file=sys.stderr)
            sys.exit(3)


        # evaluate
        pairs = list(zip(test_pairs, gold_pairs))
        
        # accuracy
        count, total = 0, 0
        for i, ((test_id, test_label), (gold_id, gold_label)) in enumerate(pairs):
            if test_id != gold_id:
                print('Line {} ids are not equal ({}, {}), aborting.'.format(i, test_id, gold_id))
                sys.exit(4)
            else:
                if test_label == gold_label:
                    count += 1
                total += 1
        print('accuracy: {:.2f}'.format(count/total))

        # f-scores
        fscores = []
        for label in LABELS:
            if label == 'green': continue
            correct, system, gold = 0, 0, 0
            for i, ((test_id, test_label), (gold_id, gold_label)) in enumerate(pairs):
                if test_id != gold_id:
                    print('Line {} ids are not equal ({}, {}), aborting.'.format(i, test_id, gold_id))
                    sys.exit(4)
                else:
                    if test_label == gold_label and test_label == label:
                        correct += 1
                        system += 1
                        gold += 1 
                    elif test_label == label and gold_label != label:
                        system += 1
                    elif test_label != label and gold_label == label:
                        gold += 1
            
            if not system:
                P = 0.0
            else:
                P = correct / system

            if not gold:
                R = 0.0
            else:
                R = correct / gold
            
            if not R and not P:
                F = 0.0
            else:
                F = 2 * (P * R) / (P + R)

            print('{}\tP R F:\t{:.2f} ({}/{})\t{:.2f} ({}/{})\t{:.2f}'.format(label, P, correct, system, R, correct, gold, F))
            fscores.append(F)

        print('macro-averaged F-score: {:.2f}'.format(sum(fscores)/len(fscores)))


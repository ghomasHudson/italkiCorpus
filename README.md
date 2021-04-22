# italkiCorpus

Dataset for the work: [On the Development of a Large Scale Corpus for Native Language Identification](https://sure.sunderland.ac.uk/id/eprint/10446/1/On%20the%20Development%20of%20Large%20Scale%20Corpus%20for%20Native%20Language%20Identification%20.pdf).


## Gathering new data
Tools provided to recreate NLI corpus from the italki website

Collect data as:

```
python scrape.py scrape arabic chinese french german hindi italian japanese korean russian spanish turkish
```

To recreate the exact same dataset as collected in 2017, pass the ID list file:

```
python scrape.py recreate 2017_ids.txt
```

## Citation
If you use this dataset in your work, please cite:
```
@inproceedings{hudson2018development,
  title={On the Development of a Large Scale Corpus for Native Language Identification},
  author={Hudson, Thomas G and Jaf, Sardar},
  booktitle={Proceedings of the 17th International Workshop on Treebanks and Linguistic Theories (TLT 2018), December 13--14, 2018, Oslo University, Norway},
  number={155},
  pages={115--129},
  year={2018},
  organization={Link{\"o}ping University Electronic Press}
}
```

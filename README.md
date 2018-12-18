# italkiCorpus



## Gathering new data
Tools provided to recreate NLI corpus from the italki website

Collect data as:

```
python scrape.py --output-dir=italkiDataset arabic chinese french german hindi italian japanese korean russian spanish turkish
```

To recreate the exact same dataset as collected in 2017, pass the URL list file as an additional argument (Not Implemented Yet):

```
python scrape.py italkiDataset 2017urls.txt
```

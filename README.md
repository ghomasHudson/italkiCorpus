# italkiCorpus ![example workflow](https://github.com/ghomasHudson/italkiCorpus/actions/workflows/python-app.yml/badge.svg)

Dataset for our work: [On the Development of a Large Scale Corpus for Native Language Identification](https://sure.sunderland.ac.uk/id/eprint/10446/1/On%20the%20Development%20of%20Large%20Scale%20Corpus%20for%20Native%20Language%20Identification%20.pdf).

*Note: The italki website has moved away from the notebooks used in this project. This code probably wont work anymore (at least till updated)*

## Gathering data
Due to copyright reasons we don't publish the raw data. Instead, tools are provided to recreate NLI corpus from the italki website.

To recreate the exact same dataset as collected in 2017, pass the ID list file:

```bash
python3 scrape.py recreate 2017_ids.txt
```

Collect your own new data using:

```bash
python3 scrape.py scrape arabic chinese french german hindi italian japanese korean russian spanish turkish
```

By default, this will make a new folder `italki_data` with `.txt` files named with their document id, as well as a label csv file:
```
document_id, author_id, L1, english_proficiency
142576, 32162, Turkish, 2
248781, 12987, French, 4
...
```
## A simple benchmark (WIP)
In the `benchmark` folder there are 2 scripts:
1. `italki/italki.py` - Loads the data using the [Huggingface Datasets](https://github.com/huggingface/datasets) library. You can reuse this for your own models.
2. `train.py` - Trains a simple bert model using the dataset.

Feel free to use and adapt these for your own research. To include the huggingface datasets version in your own script, you can write:
```python
>>> import datasets
>>> ds = datasets.load_dataset("./benchmark/italki", data="../italki_data")
>>> print(ds["train"][0])
{"document": "Today I went to...", "native_language": "French", "proficiency": 5, ...}
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

### Dataset Metadata
The following table is necessary for this dataset to be indexed by search
engines such as <a href="https://g.co/datasetsearch">Google Dataset Search</a>.
<div itemscope itemtype="http://schema.org/Dataset">
<table>
  <tr>
    <th>property</th>
    <th>value</th>
  </tr>
  <tr>
    <td>name</td>
    <td><code itemprop="name">Italki Native Language Identification Dataset</code></td>
  </tr>
  <tr>
    <td>alternateName</td>
    <td><code itemprop="alternateName">Italki</code></td>
  </tr>
  <tr>
    <td>url</td>
    <td><code itemprop="url">https://github.com/ghomasHudson/italkiCorpus</code></td>
  </tr>
  <tr>
    <td>description</td>
    <td><code itemprop="description">Native Language Identification (NLI) is the task of identifying an author’s native language from their writings in a second language. This dataset (italki) consists of large quantities of text from the language learning website italki. The italki website creates a community for language learners to access teaching resources, practice speaking, discuss topics and ask questions in their target language (the English language). We gather free-form ‘Notebook’ documents, which are mainly autobiographical diary entries with connected profiles describing the native language of the author.

This repository contains scripts to download the data along with the ids to recreate the 2017 dataset.</code></td>
  </tr>
  <tr>
    <td>citation</td>
    <td><code itemprop="citation">https://ep.liu.se/ecp/article.asp?issue=155&article=012</code></td>
  </tr>
</table>
</div>


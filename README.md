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
    <td>sameAs</td>
    <td><code itemprop="sameAs">https://github.com/ghomasHudson/italkiCorpus</code></td>
  </tr>
  <tr>
    <td>description</td>
    <td><code itemprop="description">This repository contains the italki Native Language Identification (NLI) dataset. It includes scripts to download the data along with the ids to recreate the 2017 dataset.</code></td>
  </tr>
  <tr>
    <td>citation</td>
    <td><code itemprop="citation">https://ep.liu.se/ecp/article.asp?issue=155&article=012</code></td>
  </tr>
</table>
</div>


# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Italki NLI: Native Language Identification"""


import csv
import json
import os

import datasets

_CITATION = """\
proceedings{hudson2018development,
    title={On the Development of a Large Scale Corpus for Native Language Identification},
    author={Hudson, Thomas G and Jaf, Sardar},
    booktitle={Proceedings of the 17th International Workshop on Treebanks and Linguistic Theories (TLT 2018), December 13--14, 2018, Oslo University, Norway},
    number={155},
    pages={115--129},
    year={2018},
    organization={Link{\"o}ping University Electronic Press}
}
"""

_DESCRIPTION = """\
Using italki to identify the native language of english-learners
"""

_HOMEPAGE = "https://github.com/ghomasHudson/italkiCorpus"

_LICENSE = ""

_URLs = {
    'first_domain': "https://github.com/ghomasHudson/italkiCorpus",
}


class Italki(datasets.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "document": datasets.Value("string"),
                    "document_id": datasets.Value("string"),
                    "author_id": datasets.Value("string"),
                    "native_language": datasets.ClassLabel(names=[
                        "arabic",
                        "chinese",
                        "french",
                        "german",
                        "hindi",
                        "italian",
                        "japanese",
                        "korean",
                        "russian",
                        "spanish",
                        "turkish"]),
                    "proficiency": datasets.Value("int32")
                }),
            # supervised_keys=("native_language"),
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def manual_download_instructions(self):
        return (
            "To use the italki Native Language dataset, you have to download it manually."
            "First clone the repo: https://github.com/ghomasHudson/italkiCorpus"
            "Then run `python3 scrape.py recreate 2017_ids.txt`. You can then load the"
            "dataset with:"
            "`datasets.load_dataset('italki', data_dir='path/to/folder/italkiCorpus/italki_data')`"
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))

        if not os.path.exists(data_dir):
            raise FileNotFoundError(
                "{} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('italki', data_dir=...)` that includes files downloaded using the tool. Manual download instructions: {}".format(
                    data_dir, self.manual_download_instructions
                )
            )

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": data_dir, "split": "train"}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": data_dir, "split": "dev"}
            )
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples as (key, example) tuples. """

        with open(os.path.join(filepath, "labels."+split+".csv"), encoding="utf8") as f:
            reader = csv.DictReader(f)
            for n, row in enumerate(reader):
                text = open(os.path.join(filepath, row["document_id"]+".txt"), 'r').read()

                if row["english_proficiency"] == "":
                    row["english_proficiency"] = -1
                else:
                    row["english_proficiency"] = int(row["english_proficiency"])

                yield n, {
                    "document": text,
                    "document_id": row["document_id"],
                    "author_id": row["author_id"],
                    "native_language": row["L1"],
                    "proficiency": row["english_proficiency"]
                }

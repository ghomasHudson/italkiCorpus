#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Scrape the native language and text from italki notebooks"""

import argparse
import requests
import os
import sys
import re
import csv
import glob
from multiprocessing import Pool, Lock


def save_document(doc_id, output_dir):
    '''Gather document details'''

    # Get document details
    url = "https://www.italki.com/api/notebook/"+str(doc_id)+""
    r = requests.get(url)
    if r.status_code != 200:
        print("%s not found" % str(doc_id), file=sys.stderr)
        return
    doc = {"document_id": doc_id}
    doc["content"] = r.json()["data"]["content"]

    # Get author details
    author_id = str(r.json()["data"]['author_obj']['id'])
    url = "https://www.italki.com/api/user/"+str(r.json()["data"]['author_obj']['id'])+""
    r = requests.get(url)
    if r.status_code != 200:
        print("Author with id %s not found" % author_id, file=sys.stderr)
        return
    author = r.json()['data']
    doc['author_obj'] = author
    doc["author_id"] = author["id"]

    # Find native language (Language most proficient in)
    max_prof_idx = 0
    languages = doc["author_obj"]["language_obj_s"]
    for i in range(len(languages)):
        if languages[i]["is_learning"] == 0 and languages[i]["level"] > languages[max_prof_idx]["level"]:
            max_prof_idx = i
    doc["L1"] = languages[max_prof_idx]["language"]

    # Get english proficiency
    for l in doc["author_obj"]["language_obj_s"]:
        if l["language"] == "english":
            doc["english_proficiency"] = l["level"]

    del doc["author_obj"]  # Get rid of extra info

    # Save content
    open(os.path.join(output_dir, str(doc_id) + ".txt"), 'w').write(doc["content"])
    del doc["content"]
    return doc


def drawLoadingBar(val, maximum):
    if val <= maximum:
        val = min(val, maximum)  # prevent overshooting
        maxLength = 50
        barLength = int((val/maximum)*maxLength)
        percentage = (val/maximum)*100.0
        if sys.version_info[:2] <= (2, 7):
            barStr = "|"+"█"*barLength + " "*(maxLength-barLength-1)+"|"
        else:
            barStr = "|"+"█"*barLength + "▒"*(maxLength-barLength-1)+"|"
        barStr += " " + '{0:.2f}'.format(percentage)+"%" + " (" + str(val)+"/" + str(maximum) + ")"
        print(barStr+"\r", end="")
    else:
        print()

def parse_args(args):
    print("Getting language list...")
    r = requests.get("https://www.italki.com/i18n/en_us.json?v=v1.2.0")
    languages = []
    for c in r.json().keys():
        if c.lower() == c:
            languages.append(c)

    # Parse CLI arguments
    parser = argparse.ArgumentParser(description='Download raw documents from italki.')
    parser.add_argument('-s', '--output-dir',
                        required=False,
                        default="italki_data",
                        help='Directory to output documents')
    subparsers = parser.add_subparsers(help='help for subcommand', dest="command", required=True)

    # create the parser for the "command_1" command
    parser_a = subparsers.add_parser('scrape', help='Scrape new documents from italki')
    parser_a.add_argument('-r', '--max-per-lang',
                          required=False,
                          type=int,
                          default=1000,
                          help='Maximum number of documents to be downloaded per language')
    parser_a.add_argument('languages',
                          nargs='+',
                          choices=languages,
                          help='List of languages to download')

    # create the parser for the "command_2" command
    parser_b = subparsers.add_parser('recreate', help='Recreate an existing dataset')
    parser_b.add_argument('id_file', type=argparse.FileType("r"), help='List of italki ids')
    parser_b.add_argument('--num_agents', type=int, help='Number of concurrent agents to run', default=5)

    return parser.parse_args(args)



def main(args):
    global _process_line
    # Make data dir
    try:
        os.mkdir(args.output_dir)
    except:
        print("Cannot create italki_data directory")
        sys.exit()

    if args.command == "scrape":
        with open(os.path.join(args.output_dir, "labels.csv"), 'w') as f:
            writer = csv.DictWriter(f, fieldnames=["document_id", "author_id", "L1", "english_proficiency"])
            writer.writeheader()
            for language in args.languages:
                currentCount = 0
                print()
                print(language)
                page = currentCount//15

                while currentCount < args.max_per_lang:
                    # get list of notebooks
                    api = "https://www.italki.com/api/notebook?&author_language="+language+"&language="+"english"+"&page="+str(page)
                    r = requests.get(api)

                    # Check if last page
                    if not(r.json()['meta']['has_next']):
                        print("NO MORE PAGES")
                        break

                    docs = r.json()['data']

                    for i, d in enumerate(docs):
                        if currentCount > args.max_per_lang:
                            break
                        drawLoadingBar(currentCount, args.max_per_lang)
                        currentCount += 1
                        writer.writerow(save_document(d["id"], args.output_dir))

    elif args.command == "recreate":
        lines = list(args.id_file.readlines()[1:])

        for split in ["train", "test", "dev"]:
            with open(os.path.join(args.output_dir, "labels." + split + ".csv"), 'a') as f:
                writer = csv.DictWriter(f, fieldnames=["document_id", "author_id", "L1", "english_proficiency"])
                writer.writeheader()

        indexes = []
        def _process_line(tup):
            index, line = tup
            doc_id, split = line.strip().split(",")
            doc = save_document(doc_id, args.output_dir)
            if doc is not None:
                l.acquire()
                with open(os.path.join(args.output_dir, "labels." + split + ".csv"), 'a') as f:
                    writer = csv.DictWriter(f, fieldnames=["document_id", "author_id", "L1", "english_proficiency"])
                    writer.writerow(doc)
                indexes.append(index)
                drawLoadingBar(len(glob.glob(os.path.join(args.output_dir, "*.txt"))), len(lines))
                l.release()

        def init(l):
            global lock
            lock = l

        l = Lock()
        print("start pool")
        with Pool(processes=args.num_agents, initializer=init, initargs=(l,)) as pool:
            _ = pool.map(_process_line, enumerate(lines), 1)

if __name__ == "__main__":
    main(parse_args(sys.argv[1:]))

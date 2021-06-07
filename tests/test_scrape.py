from scrape import *
import pytest
import json
import requests_mock
import csv
import os
import tempfile
import argparse
from types import SimpleNamespace

def make_mocks(doc_id, auth_id, l1, proficiency=0):
    test_document = {
        "performance": "123.4 ms",
        'meta': {
            'other_notebooks': []},
        'server_time': 0,
        'data': {
            'edited': 0,
            'language': 'english',
            'view_count': 123,
            'title': 'My First Notebook',
            'editable': 0,
            'mark_sum': 0,
            'content': "Text content for doc #" + str(doc_id),
            'audio_url': '',
            'comment_count': 0,
            'create_time': '2000-00-00T00:00:00+0000',
            'image_url': '',
            'correction_count': 0,
            'device': 0,
            'author_obj': {
                'exam_result_shown_obj': None,
                'textid': 'T1234',
                'avatar_file_name': None,
                'is_tutor': 0,
                'is_premium': 0,
                'allow_profile': 1,
                'nickname': 'myname',
                'id': auth_id,
                'is_pro': 0
            },
            'author_id': 1234,
            'id': doc_id
        }
    }
    test_author = {
        'performance': '123.4 ms',
        'meta': {},
        'server_time': 1234,
        'id': auth_id,
        'data': {
            'learning_language': 'english',
            'language_obj_s': [
                {
                    'can_teach': 0,
                    'language': 'english',
                    'level': proficiency,
                    'priority': 2,
                    'is_teaching': 0,
                    'is_learning': 1,
                    'id': 1234},
                {
                    'can_teach': 0,
                    'language': l1,
                    'level': 7,
                    'priority': 1,
                    'is_teaching': 0,
                    'is_learning': 0,
                    'id': 1235
                }
            ],
            'gender': 2,
            'age': 0,
            'show_dob': 0,
            'id': auth_id,
        }
    }
    return test_document, test_author

def test_save_document_normal():
    '''Tests that we can save a document given the id'''
    with requests_mock.Mocker()as m:
        with tempfile.TemporaryDirectory() as tmpdirname:
            csv_filename = os.path.join(tmpdirname, "test.csv")
            with open(csv_filename, 'w') as f:
                writer = csv.DictWriter(f, fieldnames=["document_id", "author_id", "L1", "english_proficiency"])
                test_document, test_author = make_mocks("1234", "1234", "hindi")
                m.get("https://www.italki.com/api/notebook/1234", text=json.dumps(test_document))
                m.get("https://www.italki.com/api/user/1234", text=json.dumps(test_author))
                save_document("1234", tmpdirname, writer)
            assert open(csv_filename).read() == "1234,1234,hindi,0\n"
            assert open(os.path.join(tmpdirname, "1234.txt")).read() == test_document["data"]["content"]


def test_save_document_404():
    '''Tests that we can handle a 404'''
    with requests_mock.Mocker() as m:
        with tempfile.TemporaryDirectory() as tmpdirname:
            csv_filename = os.path.join(tmpdirname, "test.csv")
            with open(csv_filename, 'w') as f:
                writer = csv.DictWriter(f, fieldnames=["document_id", "author_id", "L1", "english_proficiency"])
                m.get("https://www.italki.com/api/notebook/1234", status_code=404)
                save_document("1234", tmpdirname, writer)
            assert open(csv_filename).read() == ""
            assert not os.path.isfile(os.path.join(tmpdirname, "1234.txt"))


def test_parser():
    parser = parse_args(["scrape", "french", "italian"])
    assert parser.command == "scrape"
    assert parser.languages == ["french", "italian"]
    parser = parse_args(["recreate", "2017_ids.txt"])
    assert parser.command == "recreate"
    assert parser.id_file.name == "2017_ids.txt"

def test_recreate():
    with requests_mock.Mocker() as m:
        with tempfile.TemporaryDirectory() as tmpdirname:
            id_filename = os.path.join(tmpdirname, "test_ids.txt")
            with open(id_filename, 'w') as f:
                f.write("id,set\n")
                f.write("1,train\n")
                f.write("2,test\n")
                f.write("3,dev\n")
                f.write("4,train\n")
            test_document1, test_author = make_mocks("1", "1234", "hindi")
            test_document2, _ = make_mocks("2", "1234", "hindi")
            test_document3, _ = make_mocks("3", "1234", "hindi")
            test_document4, test_author4 = make_mocks("4", "12344", "french", proficiency=5)
            m.get("https://www.italki.com/api/user/1234", text=json.dumps(test_author))
            m.get("https://www.italki.com/api/user/12344", text=json.dumps(test_author4))
            m.get("https://www.italki.com/api/notebook/1", text=json.dumps(test_document1))
            m.get("https://www.italki.com/api/notebook/2", text=json.dumps(test_document2))
            m.get("https://www.italki.com/api/notebook/3", text=json.dumps(test_document3))
            m.get("https://www.italki.com/api/notebook/4", text=json.dumps(test_document4))
            main(SimpleNamespace(
                command="recreate",
                agents=1,
                output_dir=os.path.join(tmpdirname, "output"),
                id_file=open(os.path.join(tmpdirname, "test_ids.txt"))
            ))
            assert open(os.path.join(tmpdirname, "output", "1.txt")).read() == test_document1["data"]["content"]
            assert open(os.path.join(tmpdirname, "output", "2.txt")).read() == test_document2["data"]["content"]
            assert open(os.path.join(tmpdirname, "output", "3.txt")).read() == test_document3["data"]["content"]
            assert open(os.path.join(tmpdirname, "output", "4.txt")).read() == test_document4["data"]["content"]
            assert open(os.path.join(tmpdirname, "output", "labels.train.csv")).read() == "document_id,author_id,L1,english_proficiency\n1,1234,hindi,0\n4,12344,french,5\n"
            assert open(os.path.join(tmpdirname, "output", "labels.test.csv")).read() == "document_id,author_id,L1,english_proficiency\n2,1234,hindi,0\n"
            assert open(os.path.join(tmpdirname, "output", "labels.dev.csv")).read() == "document_id,author_id,L1,english_proficiency\n3,1234,hindi,0\n"

def test_scrape():
    pass

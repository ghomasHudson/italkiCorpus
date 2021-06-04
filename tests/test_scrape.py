from scrape import *
import json
import requests_mock
import csv
import os
import tempfile


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
        'content': "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
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
            'id': 1234,
            'is_pro': 0
        },
        'author_id': 1234,
        'id': 1234
    }
}
test_author = {
    'performance': '123.4 ms',
    'meta': {},
    'server_time': 1234,
    'id': 1234,
    'data': {
        'learning_language': 'english',
        'language_obj_s': [
            {
                'can_teach': 0,
                'language': 'english',
                'level': 0,
                'priority': 2,
                'is_teaching': 0,
                'is_learning': 1,
                'id': 1234},
            {
                'can_teach': 0,
                'language': 'hindi',
                'level': 7,
                'priority': 1,
                'is_teaching': 0,
                'is_learning': 0,
                'id': 1234
            }
        ],
        'gender': 2,
        'age': 0,
        'show_dob': 0,
        'id': 1234,
    }
}

def test_save_document():
    '''Tests that we can save a document given the id'''
    with requests_mock.Mocker()as m:
        with tempfile.TemporaryDirectory() as tmpdirname:
            csv_filename = os.path.join(tmpdirname, "test.csv")
            with open(csv_filename, 'w') as f:
                writer = csv.DictWriter(f, fieldnames=["document_id", "author_id", "L1", "english_proficiency"])
                m.get("https://www.italki.com/api/notebook/1234", text=json.dumps(test_document))
                m.get("https://www.italki.com/api/user/1234", text=json.dumps(test_author))
                save_document("1234", tmpdirname, writer)
            assert open(csv_filename).read() == "1234,1234,hindi,0\n"
            assert open(os.path.join(tmpdirname, "1234.txt")).read() == test_document["data"]["content"]




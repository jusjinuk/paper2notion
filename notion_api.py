from lib2to3.pgen2 import token
from argument import args
from notion_client import Client
from pprint import pprint

from main import PaperRecord


def upload_paper(rec):
    notion = Client(auth=args.token)
    id = f'{args.id[:8]}-{args.id[8:12]}-{args.id[12:16]}-{args.id[16:20]}-{args.id[20:]}'
    my_page = notion.pages.create(
        **{
            'parent': {
                'database_id': id,
                'type': 'database_id'
            },
            'properties': {
                'Author': {
                    'rich_text': [{
                        'text': {
                            'content': rec.author
                        },
                        'type': 'text'
                    }],
                },
                'FileName': {
                    'rich_text': [{
                        'text': {
                            'content': rec.file,
                        },
                        'type': 'text'
                    }],
                },
                'Title': {
                    'title': [{
                        'text': {
                            'content': rec.title,
                        },
                        'type': 'text'
                    }],
                    'type': 'title'
                },
                'Year': {
                    'number': rec.year,
                    'type': 'number'
                }
            },
            'children': [
                {
                    'object': 'block',
                    'type': 'heading_2',
                    'heading_2': {
                        'text': [{
                            'type': 'text',
                            'text': {
                                'content': 'Summary'
                            }
                        }]
                    },
                },
                {
                    'object': 'block',
                    'type': 'paragraph',
                    'paragraph': {
                        'text': [{
                            'type': 'text',
                            'text': {
                                'content': ''
                            }
                        }]
                    },
                },
                {
                    'object': 'block',
                    'type': 'heading_2',
                    'heading_2': {
                        'text': [{
                            'type': 'text',
                            'text': {
                                'content': 'Novelty'
                            }
                        }]
                    },
                },
                {
                    'object': 'block',
                    'type': 'paragraph',
                    'paragraph': {
                        'text': [{
                            'type': 'text',
                            'text': {
                                'content': ''
                            }
                        }]
                    },
                },
                {
                    'object': 'block',
                    'type': 'heading_2',
                    'heading_2': {
                        'text': [{
                            'type': 'text',
                            'text': {
                                'content': 'Note'
                            }
                        }]
                    },
                },
                {
                    'object': 'block',
                    'type': 'paragraph',
                    'paragraph': {
                        'text': [{
                            'type': 'text',
                            'text': {
                                'content': ''
                            }
                        }]
                    },
                },
            ],
        })

    # response = notion.search(sort={
    #     'direction': 'ascending',
    #     'timestamp': 'last_edited_time'
    # })
    # pprint(response)


if __name__ == "__main__":
    rec = PaperRecord('author22another.pdf', 'Another Example Paper2',
                      'Example Author', 2022)
    upload_paper(rec)

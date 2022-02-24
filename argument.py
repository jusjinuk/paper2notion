import argparse

parser = argparse.ArgumentParser(description='Arguments for Paper2Notion')
parser.add_argument('path',
                    metavar='Path',
                    type=str,
                    help='file path of the paper')
parser.add_argument('--token',
                    metavar='Notion Token',
                    type=str,
                    required=True,
                    help='Token for Notion')
parser.add_argument('--id',
                    metavar='Notion Page Id',
                    type=str,
                    required=True,
                    help='Page Id for Notion')

args = parser.parse_args()

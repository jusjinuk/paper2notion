import argparse


def str2bool(v):
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')


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
parser.add_argument('--verbose',
                    metavar='Verbose',
                    help='Whether you are going to see font family',
                    type=str2bool,
                    default=False)

args = parser.parse_args()

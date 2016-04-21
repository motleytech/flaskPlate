import argparse


parser = argparse.ArgumentParser(description='Process input.')
parser.add_argument('--host', dest='host', default='0.0.0.0',
                   help='host address')

args = parser.parse_args()
print args.host

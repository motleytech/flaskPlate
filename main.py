#!/usr/bin/env python
"""
fun stuff
"""

import argparse
from app import app

parser = argparse.ArgumentParser(description='Process input.')
parser.add_argument('--host', dest='host', default='0.0.0.0',
                   help='host address')
parser.add_argument('--port', dest='port', default=5000,
                   help='port')
args = parser.parse_args()

print "Starting server on %s:%s..." % (args.host, args.port)
app.run(debug=True, host=args.host, port=args.port)

"""Dos: python writer.py | reader.py."""

import sys

print('Got this: "%s"' % input())
data = sys.stdin.readline()[:-1]
print('The meaning of life is', data, int(data) * 2)

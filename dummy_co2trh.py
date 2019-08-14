#!/usr/bin/env python3

"""Spits out fake readings, good for testing

"""

import random
import time

READINGS_RAW = """
42.6 27.3 47.5
22.3 27.4 47.2
0.4 27.4 46.9
28.3 27.4 46.7
513.6 27.4 46.7
33.6 27.4 46.7
485.6 27.4 46.6
26.7 27.3 46.9
477.5 27.4 46.9
35.7 27.4 47.4
14.9 27.4 47.3
454.1 27.3 46.9
449.4 27.3 46.8
449.7 27.3 46.7
329.0 27.3 48.8
260.8 27.3 47.4
191.2 27.2 47.1
60.4 27.2 47.2
55.3 27.2 47.2
26.8 27.2 47.2
25.2 27.2 47.1
476.8 27.2 47.7
3.0 27.2 47.5
602.1 0.0 0.0
11.8 27.2 47.3
32.3 27.2 47.4
0.5 27.2 47.1
421.3 27.3 46.9
437.0 27.3 47.0
8.3 27.4 47.2
29.6 27.3 47.1
19.9 27.4 47.0
438.4 27.4 46.7
21.8 27.4 47.0
470.9 27.3 46.7
60.7 27.3 46.8
19.1 27.2 47.2
464.1 27.2 47.5
34.1 27.3 47.4
55.9 27.3 47.4
83.2 27.3 47.4
48.9 27.3 47.4
61.1 27.2 47.4
24.5 27.2 47.3
38.9 27.2 47.5
15.7 27.3 47.6
13.5 27.2 47.4
31.4 27.2 47.8
36.7 27.2 47.6
61.9 27.2 48.0
1.3 27.2 47.8
3.6 27.3 47.9
15.0 27.3 47.9
482.5 27.3 47.6
27.8 27.2 47.4
49.3 27.3 47.3
427.6 27.3 47.2
43.4 27.2 47.3
44.9 27.3 47.8
38.5 27.3 47.9
329.9 27.2 49.1
423.0 27.3 49.3
"""
READINGS_LINES = [line.strip() for line in READINGS_RAW.splitlines() if line.strip()]

if __name__ == "__main__":
    line = random.choice(READINGS_LINES)
    time.sleep(2.1)
    print(line)

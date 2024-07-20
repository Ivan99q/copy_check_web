import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

from sql_script.mysql_op import *
from sql_script.postgresql_op import *
from sql_script.vector import *
from init_database.ckg import *

import time
import numpy as np
import datetime

sentence = [
    i[0] for i in postgresql_execute("select sentence from corpus_sentence limit 1000")
]

t = []
for s in sentence:
    start = time.time()
    vector(s)
    end = time.time()
    running_time = end - start
    t.append(running_time)

print(datetime.timedelta(seconds=np.mean(t)))

from operator import itemgetter
import sys

current_key = None
current_count = 0
key = None

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    key, count = line.split('\t', 1)

    count = int(count)

    # stream and sort
    if current_key == key:
        current_count += count
    else:
        if current_key:
            # write result to STDOUT
            print '%s\t%s' % (current_key, current_count)
        current_count = count
        current_key = key

# do not forget to output the last key if needed!
if current_key == key:
    print '%s\t%s' % (current_key, current_count)


# hadoop
#
#
# hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar -input /user/ds222/assignment-1/DBPedia.full/full_train.txt -output output -mapper mapper.py -reducer reducer.py -file mapper.py -file reducer.py
# 
#  /user/ds222/assignment-1/DBPedia.full/

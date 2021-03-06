"""
 Compute Pi on a cluster.

 It is not recommended to run this application from the IDE.

 @author rambabu.posa
"""
import time
from pyspark.sql import SparkSession
from random import random
from operator import add

slices = 10
numberOfThrows = 100000 * slices
print("About to throw {} darts, ready? Stay away from the target!".format(numberOfThrows))

t0 = int(round(time.time() * 1000))

spark = SparkSession.builder.appName("PySparkPi on a cluster") \
    .master("spark://un:7077").getOrCreate()
    #.master("local[*]").getOrCreate()

t1 = int(round(time.time() * 1000))

print("Session initialized in {} ms".format(t1 - t0))

numList = []

for x in range(numberOfThrows):
    numList.append(x)

incrementalRDD = spark.sparkContext.parallelize(numList)

t2 = int(round(time.time() * 1000))
print("Initial dataframe built in {} ms".format(t2 - t1))

def throwDarts(_):
    x = random() * 2 - 1
    y = random() * 2 - 1
    return 1 if x ** 2 + y ** 2 <= 1 else 0

dartsRDD = incrementalRDD.map(throwDarts)

t3 = int(round(time.time() * 1000))
print("Throwing darts done in {} ms".format(t3 - t2))

dartsInCircle = dartsRDD.reduce(add)
t4 = int(round(time.time() * 1000))

print("Analyzing result in {} ms".format(t4 - t3))

print("Pi is roughly {}".format(4.0 * dartsInCircle/numberOfThrows))

spark.stop()
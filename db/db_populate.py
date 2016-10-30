import psycopg2
from states import state_abbreviations

try:
    conn = psycopg2.connect("dbname='twitter_sent_analysis' user='antonis' host='localhost' port='5433' password='123456'")
except:
        print "I am unable to connect to the database"

cur = conn.cursor()

for key in state_abbreviations.keys():
    cur.execute("INSERT INTO sentiment VALUES('%s', 0, 0)" % key)

conn.commit()


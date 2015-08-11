import sys
import sqlite3
import datetime

QUERY = "select personal || ' ' || family from workshops_person where username=?;"

COMMAND = "python bin/certificates.py -i /Applications/Inkscape.app/Contents/Resources/bin/inkscape -s $PWD/instructor.svg -o $PWD/instructor/{0}.pdf date='{1}' instructor='Greg Wilson' name='{2}'"

connection = sqlite3.connect(sys.argv[1])
cursor = connection.cursor()

for pid in sys.stdin:
    pid = pid.strip()
    cursor.execute(QUERY, [pid])
    try:
        name = cursor.fetchall()[0][0]
        d = datetime.datetime.today().strftime('%B %-e, %Y')
        print COMMAND.format(pid, d, name)
    except Exception, e:
        print 'failed on {0}: {1}'.format(pid, str(e))

cursor.close()
connection.close()


import sys
import sqlite3
import datetime

QUERY = "select person.personal || ' ' || person.family, awards.awarded from person join awards on person.person=awards.person where person.person=? and awards.badge='instructor';"

COMMAND = "python bin/certificates.py -i /Applications/Inkscape.app/Contents/Resources/bin/inkscape -s $PWD/instructor.svg -o $PWD/instructor/{0}.pdf date='{1}' instructor='Greg Wilson' name='{2}'"

connection = sqlite3.connect(sys.argv[1])
cursor = connection.cursor()

for pid in sys.stdin:
    pid = pid.strip()
    cursor.execute(QUERY, [pid])
    name, d = cursor.fetchall()[0]
    d = datetime.datetime(*[int(x) for x in d.split('-')])
    d = d.strftime("%B %-e, %Y")
    print COMMAND.format(pid, d, name)

cursor.close()
connection.close()


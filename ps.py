#!/usr/bin/env python3
"""
Update songs database and render static page
http://www.sqlitetutorial.net/sqlite-python/
"""
import re
import sys
import datetime
import logging
import sqlite3
from urllib.request import urlopen


logging.basicConfig(level=logging.DEBUG)

TABLE_SCHEMA = """\
    CREATE TABLE songs (\
    id integer primary key not null, \
    name char(100), \
    performer char(100), \
    descr text, \
    url text, \
    added date);
    """

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('songs.db')
        self.curr = self.conn.cursor()

    def init_db(self):
        self.curr.executescript(TABLE_SCHEMA)

    def add(self, song):
        self.curr.execute(
            """INSERT INTO songs \
                (name, performer, descr, url, added) \
                VALUES (?, ?, ?, ?, ?)""", song)
        self.conn.commit()

    def get_songs(self):
        songs = []
        for row in self.conn.execute('SELECT * FROM songs;'):
            songs.append(row)
        return songs

    def __del__(self):
        self.conn.close()
        

def add_item(link):
    """Load page ang extract title. Save to db."""
    logging.debug('Add item :> {}'.format(link))
    request = urlopen(link)
    data = request.read()

    t_length = len('<title>')
    from_idx = data.find(b'<title>')
    to_idx = data.find(b'</title>')

    result = data[from_idx+t_length:to_idx]
    print(result)
    
    # Clear block XXX TODO extract to function
    result = result.rstrip(b' - YouTube')
    result = result.rstrip(b'(Official Video)')
    result = re.sub(b'\&\#.+;', b'', result)

    # XXX extract to the function
    if result.count(b' - ') == 1:
        logging.debug('Detected exactly one <dash> in the title')
        parts = re.split(b' - ', result)
        variant_direct = "{} - {}".format(parts[0], parts[1])
        variant_reverse = "{} - {}".format(parts[1], parts[0])
        print('Variants are:\n 1: {}\n 2: {}'.format(
            variant_direct,
            variant_reverse)
        )
        select = input('Which variant is in format <Title> - <Performer>?: ')
        if select == '1':
            print(variant_direct)
        else:
            print(variant_reverse)
        return

    pattern = b'\s'
    for counter, word in enumerate(re.split(pattern, result)):
        print("{}: {}".format(counter, word))


def render_db():
    """Generate static page based on db."""
    logging.debug('Render db')
    db = DB()
    songs = db.get_songs()
    print(songs)


def interactive():
    """Enter data manualy."""
    logging.debug('Interactive mode entered')
    db = DB()
    # db.init_db()

    name = input('Title is: ')
    performer = input('Performer is: ')
    descr = input('Description is: ')
    url = input('Url is: ')
    date = datetime.date.today()

    song = (name, performer, descr, url, date)

    db.add(song)


if __name__ == '__main__':
    args = sys.argv
    if len(args) > 1:
        cmd = args[1] 
        if cmd in ['add', 'a']:
            if len(args) > 2:
                add_item(args[2])
            else:
                logging.info('Provide more arguments for a[dd] command')
        elif cmd in ['render', 'r']:
            render_db()
    else:
        interactive()

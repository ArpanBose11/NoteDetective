#!/usr/bin/python
from libs.db_sqlite import SqliteDatabase
import os, shutil

if __name__ == '__main__':
    db = SqliteDatabase()

    # songs table
    db.query("DROP TABLE IF EXISTS songs;")
    print('removed db.songs')

    db.query("""
    CREATE TABLE songs (
      id  INTEGER PRIMARY KEY AUTOINCREMENT,
      name  TEXT,
      filehash  TEXT,
      genre TEXT,
      artist TEXT,
      albumart BLOB,
      album TEXT
    );
  """)
    print('created db.songs')

    # fingerprints table

    db.query("DROP TABLE IF EXISTS fingerprints;")
    print('removed db.fingerprints')

    db.query("""
    CREATE TABLE `fingerprints` (
      `id`  INTEGER PRIMARY KEY AUTOINCREMENT,
      `song_fk` INTEGER,
      `hash`  TEXT,
      `offset`  INTEGER
    );
  """)
    print('created db.fingerprints')

    count = int(3)
    folder = 'plots/'
    while count != 0:
        folder = folder + 'peaks'
        if count == 2:
            folder = 'plots/signal'
        if count == 1:
            folder = 'plots/spectogram'
        count -= 1
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    print('Finished resetting')

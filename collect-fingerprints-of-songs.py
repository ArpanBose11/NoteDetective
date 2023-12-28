#!/usr/bin/python
import os

from termcolor import colored
import libs.fingerprint as fingerprint
from libs.config import get_config
from libs.db_sqlite import SqliteDatabase
from libs.reader_file import FileReader
from tinytag import TinyTag
from PIL import Image
import io

if __name__ == '__main__':
    config = get_config()

    db = SqliteDatabase()
    path = "mp3/"

    # fingerprint all files in a directory

    for filename in os.listdir(path):
        if filename.endswith(".mp3") or filename.endswith(".flac") or filename.endswith(".wav"):

            reader = FileReader(path + filename)
            audio = reader.parse_audio()
            # Metadata storage
            metadata = []
            a_tag = TinyTag.get(path + filename, image=True)
            image_data = a_tag.get_image()
            #pi = Image.open(io.BytesIO(image_data))  #for viewing image

            metadata.append(a_tag.artist)
            metadata.append(a_tag.albumartist)
            metadata.append(a_tag.genre)
            metadata.append(a_tag.album)
            #db.store_metadata(metadata)

            song = db.get_song_by_filehash(audio['file_hash'])
            song_id = db.add_song(filename, audio['file_hash'],metadata,image_data)

            msg = ' * %s %s: %s' % (
                colored('id=%s', 'white', attrs=['dark']),  # id
                colored('channels=%d', 'white', attrs=['dark']),  # channels
                colored('%s', 'white', attrs=['bold'])  # filename
            )
            print(msg % (song_id, len(audio['channels']), filename))

            if song:
                hash_count = db.get_song_hashes_count(song_id)

                if hash_count > 0:
                    msg = '   already exists (%d hashes), skip' % hash_count
                    print(colored(msg, 'red'))

                    continue

            print(colored('   new song, going to analyze..', 'green'))

            hashes = set()
            channel_amount = len(audio['channels'])

            for channeln, channel in enumerate(audio['channels']):
                msg = '   fingerprinting channel %d/%d'
                print(colored(msg, attrs=['dark']) % (channeln + 1, channel_amount))

                channel_hashes = fingerprint.fingerprint(filename,channel, Fs=audio['Fs'],
                                                         plots=config['fingerprint.show_plots'])
                channel_hashes = set(channel_hashes)

                msg = '   finished channel %d/%d, got %d hashes'
                print(colored(msg, attrs=['dark']) % (channeln + 1, channel_amount, len(channel_hashes)))

                hashes |= channel_hashes

            msg = '   finished fingerprinting, got %d unique hashes'


            values = []
            for hash, offset in hashes:
                values.append((song_id, hash, offset))

            msg = '   storing %d hashes in db' % len(values)
            print(colored(msg, 'green'))
            db.store_fingerprints(values)






    print('end')

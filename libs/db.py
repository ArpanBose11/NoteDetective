class Database(object):
    TABLE_SONGS = None
    TABLE_FINGERPRINTS = None

    def connect(self):
        pass

    def insert(self, table, params):
        pass

    def get_song_by_filehash(self, filehash):
        return self.findOne(self.TABLE_SONGS, {"filehash": filehash})

    def get_song_by_id(self, id):
        return self.findOne(self.TABLE_SONGS, {"id": id})
    def get_genre_by_id(self, id):
        return self.findOne(self.TABLE_SONGS, {"id": id})


    def add_song(self, filename, filehash, metadata,image_data):
        song = self.get_song_by_filehash(filehash)

        if not song:
            song_id = self.insert(self.TABLE_SONGS,
                                  {"name": filename, "filehash": filehash, "genre":metadata[2], "artist":metadata[0] ,"albumart":image_data,"album":metadata[3]})
        else:
            song_id = song[0]

        return song_id

    def get_song_hashes_count(self, song_id):
        pass

    def store_fingerprints(self, values):
        self.insertMany(self.TABLE_FINGERPRINTS,
                        ['song_fk', 'hash', 'offset'], values)
    def store_metadata(self,metadata):
        self.insertMany(self.TABLE_SONGS,
                        ['artist','albumartist','genre'], metadata)


import json
from lyricsgenius import Genius

CLIENT_ID="fMEEMxCIlLRv6mn4FBsKk_eDDTR3Y0_cMkDt4zC5434iE0XhRn-QzzvgtpNIuFSd"
CLIENT_SECRET="vq7_wVj8XZAO6eVrdvtb0jNGhrkv1Fl9qwiD1claAhQD80_yvUnUpDV03j60kxGi9kwL0Wfi3PeB1VMZ4vZcRg"
CLIENT_ACCESS_TOKEN="pCgIOvoAnE1lYO2v5bwvFQGbPDWpyChM4iCTu6174fWJ9kJzmZJ3L1VrFkBe91rR"


genius = Genius(CLIENT_ACCESS_TOKEN)


def saveAlbumLyricsJSON(name, artist):
    album = genius.search_album(name=name, artist=artist)
    album.save_lyrics(f'{name} By {artist}')


def CleanJSON(album, artist):
    with open(f'{album} By {artist}.json', 'r', encoding='utf-8') as f:
        albumJSON=json.loads(f.read())

        title=albumJSON['full_title']
        cover=albumJSON['cover_art_url']
        tracks=albumJSON['tracks']
        songID= [track['song']['id'] for track in tracks]
        songs = [track['song']['title'] for track in tracks]
        lyrics = [track['song']['lyrics'] for track in tracks]
        
        with open(f'{album} By {artist}.md', 'w',  encoding='utf-8') as f2:    
            f2.write(f"# {title}")
            f2.write(f"![]({cover})")
            f2.write(f"Total Songs: {len(songs)}")
            f2.write("\n___________________")
            
            zipper=zip(songID, songs, lyrics)
            for songID, song, lyrics in zipper:
                f2.write(f"\n ## {song}")
                f2.write(f"\n")
                f2.write(lyrics)
                # getSongAnnotations(song_id=songID)
                
                """
                ANNOTATION PART
                """
                myDict={}
                annotationsList=genius.song_annotations(song_id=songID, text_format='markdown')
                for annotation in annotationsList:
                    lyric, explanation= annotation
                    explanation=explanation[0][0]
                    myDict[lyric]=explanation    
                
                for key, value in myDict.items():
                    f2.write(f'\n#### {key}')
                    f2.write('\n```ANNOTATION:```\n')
                    f2.write(f'>{value}')
                    f2.write('\n\n\n')
                
                
                f2.write("\n___________________")


albumname=input("Enter the album name: ")
artistname=input("Enter the artist name: ")
saveAlbumLyricsJSON(albumname, artistname)
CleanJSON(albumname, artistname)

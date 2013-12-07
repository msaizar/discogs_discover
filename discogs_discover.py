import argparse
import requests
import urllib


def main():
    api_url = 'http://api.discogs.com'
    www_url = 'http://www.discogs.com'

    parser = argparse.ArgumentParser()
    parser.add_argument("artist", help="Artist you want to discover")

    args = parser.parse_args()
    labels = set()
    
    payload = {'type': 'artist', 'q': args.artist}
    artist_query = requests.get('%s/database/search' % api_url, params=payload)
    if artist_query.json()['pagination']['items'] > 0:
        #Grab the first artists releases
        artist = artist_query.json()['results'][0]
        releases_query = requests.get("%s/artists/%s/releases" % (api_url, artist['id']))
        if releases_query.json()['pagination']['items'] > 0:
            for release in releases_query.json()['releases']:
                #Make sure its not a master release, and that its a 12" inch release
                if release['type'] != 'master' and "12" in release['format']:
                    #Multiple labels can come comma separated
                    label_array = release['label'].split(', ')
                    for x in label_array:
                        labels.add(x.encode('utf-8'))
            if len(labels) > 0:
                print "\n%s has released records on the following labels: " % artist['title']                
                for label in labels:
                    print '%s - %s/label/%s' % (label, www_url, urllib.quote_plus(label))
    else:
        print "%s not found!" % args.artist    
    
    
if __name__ == "__main__":
    main()
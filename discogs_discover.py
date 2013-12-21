import argparse
import requests
import urllib
import os
import platform


api_url = 'http://api.discogs.com'
www_url = 'http://www.discogs.com'

def get_and_print_artist_info(artist_name):
    labels = set()
    payload = {'type': 'artist', 'q': artist_name}
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
                print "\n%s has released no records." % artist['title'] 
    else:
        print "%s not found!" % args.artist

    
def main():
    system = platform.system()
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=False)

    group.add_argument("-a", "--artist")
    group.add_argument('-i', '--interactive', action='store_true')
    args = parser.parse_args()
    if args.interactive:
        while(1):
            os.system('cls') if system == 'Windows' else os.system('clear')
                
            print "Enter artist you want to know more about: "

            artist = raw_input()
            get_and_print_artist_info(artist)
            enter = raw_input()
        
    else:
        get_and_print_artist_info(args.artist)
        exit(0)
    
    
if __name__ == "__main__":
    main()
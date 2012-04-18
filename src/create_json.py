from mutagen import File
import argparse
import json
import os


def configure():
    parser = argparse.ArgumentParser(
            description='Collect tags from media files and output as json')
    parser.add_argument(
            'filenames',
            metavar='files',
            nargs='+',
            type=str,
            help='files to be processed')

    args = parser.parse_args()
    return args.filenames


def find_tags(filename):
    try:
        media_file = File(filename, easy=True)
    except:
        print "Error extracting data from file %s" % filename

    return media_file


def build_metadata_dict(filename, metadata):
    entry = {}
    json_keys = ['artist', 'album', 'title', \
            'license', 'url', 'audacity', 'time']

    audio_filename, audio_extension = \
            os.path.splitext(os.path.basename(filename))
    for i in json_keys:
        entry[i] = 'test'

    try:
        entry['artist'] = metadata['artist'][0]
        entry['title'] = metadata['title'][0]
        entry['album'] = metadata['album'][0]
        entry['time'] = '00:11'
        entry['audacity'] = audio_filename

        if 'copyright' in metadata:
            if 'jamendo.com' in metadata['copyright'][0]:
                space_split_metadata = metadata['copyright'][0].split(' ')
                entry['url'] = space_split_metadata[-1]
                cc_license_url = [s for s in space_split_metadata \
                        if 'creativecommons' in s][0]
                cc_license = str((cc_license_url.split('/')[4])).upper()
                entry['license'] = cc_license

        if 'comment' in metadata:
            if 'magnatune.com' in metadata['comment'][0]:
                entry['url'] = metadata['comment'][0]
                entry['license'] = 'BY-NC-SA'
    except Exception, e:
        print "Error building metadata: %s" % e

    return entry


def main():
    metadata_array = []
    filenames = configure()
    for filename in filenames:
        metadata = find_tags(filename)
        metadata_array.append(build_metadata_dict(filename, metadata))

    print(json.dumps((metadata_array), sort_keys=True, indent=4))

if __name__ == '__main__':
    main()

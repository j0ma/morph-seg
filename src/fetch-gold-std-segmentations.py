import requests
import click
import sys
import os

def fetch_segmentation(word, sep=' '):
    API_KEY = os.environ['LINGUA_ROBOT_API_KEY']
    url = f"https://lingua-robot.p.rapidapi.com/language/v1/entries/en/{word}"
    headers = {
        'x-rapidapi-host': "lingua-robot.p.rapidapi.com",
        'x-rapidapi-key': f"{API_KEY}"
        }
    response = requests.request("GET", url, headers=headers)
    response_json = response.json()
    entries = response_json['entries']
    if len(entries) == 0:
        return None, None
    entry = entries[0]
    interpretations = entry['interpretations'][0]
    if 'morphemes' in interpretations:
        segmentation = sep.join([m['entry'].replace("-", "") for m in interpretations['morphemes']])
    else:
        segmentation = word
    return word, segmentation

@click.command()
@click.option('-i', required=True)
@click.option('-o', required=True)
@click.option('-s', '--separator', default='+', required=False)
def main(i, o, separator):
    with open(i, 'r') as f:
        WORDS = [w.strip() for w in f.readlines() if w.strip != '']
        OUTPUT = []
        for ix, w in enumerate(WORDS, start=1):
            _w, s = fetch_segmentation(w, sep=separator)
            if s is None:
                print(f'Nothing found for "{w}"! Skipping...')
                continue
            row = f'{w}\t{s}'
            OUTPUT.append(row)
            print(f"({ix}/{len(WORDS)})\t" + row)

        print(f'Done! Writing to {o}')
        with open(o, 'w') as f:
            f.write("\n".join(OUTPUT))

if __name__ == '__main__':
    main()

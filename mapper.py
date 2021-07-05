import os
import sys
import json
from bs4 import BeautifulSoup
from nltk.corpus import wordnet as wn
from nltk.corpus import framenet as fn

VERBNET_PATH = './verbnet/verbnet3.3/'
SEMLINK_PATH = './semlink/instances/vn-fn2.json'

def generate_csv(output='semlink-mappings.csv', vn_path=VERBNET_PATH, sl_path=SEMLINK_PATH):
    output_set = set()

    with open(sl_path) as sl:
        semlink = json.loads(sl.read())

    verbnet = {}
    for filename in os.listdir(vn_path):
        with open(f"{vn_path}{filename}") as xml:
            soup = BeautifulSoup(xml, "lxml-xml")
            key = filename.split('.xml')[0].split('-')[1]
            verbnet[key] = soup

    for key in semlink.keys():
        soup = verbnet[key.split('-')[0]]
        if len(soup.find_all('VNSUBCLASS')) == 0:
            member = soup.find('MEMBER', attrs={'name':key.split('-')[-1]})
        else:
            keyname = soup.find('VNCLASS').attrs['ID'].split('-')[0]
            newname = f"{keyname}-{'-'.join(key.split('-')[:-1])}"
            subsoup = soup.find(attrs={'ID':newname})
            member = subsoup.find('MEMBER', attrs={'name': key.split('-')[-1]})

        for option in member.attrs['wn'].replace('?', '').split(' '):           
            if len(option) > 1:
                wn_syn = wn.synset_from_sense_key(f"{option}::")
                wn_of = wn.ss2of(wn_syn).replace('-','')

                for val in semlink[key]:
                    if val == 'Appearance':
                        value = 'Give_impression'
                    elif val == 'Transition_to_a_state':
                        value = 'Transition_to_state'
                    elif val == 'Cause_of_temperature':
                        value = 'Cause_temperature_change'
                    else:
                        value = val
                    frame = fn.frame_by_name(value)
                    converted_name = '.'.join(wn_syn.name().split('.')[:-1])
                    did_something = False
                    for lemma in wn_syn.lemmas():
                        converted_name = f'{lemma.name()}.v'
                        if converted_name in frame.lexUnit:
                            lu_id = frame.lexUnit[converted_name].ID
                            output_set.add((wn_of, lu_id))
                            did_something = True
                    if not did_something:
                        for lemma in wn_syn.lemmas():
                            for lunit in frame.lexUnit:
                                if lunit.startswith(f"{lemma.name()} ") and lunit.endswith('.v'):
                                    lu_id = frame.lexUnit[lunit].ID
                                    output_set.add((wn_of, lu_id))
                                    break

    with open(output, 'w+') as out:
        for pair in sorted(list(output_set)):
            out.write(f"{pair[0]}, {pair[1]}\n")

if __name__ == '__main__':
    if len(sys.argv) == 1:
        generate_csv()
    elif len(sys.argv) == 2:
        generate_csv(output=sys.argv[-1])
    elif len(sys.argv) == 4:
        generate_csv(output=sys.argv[-3], vn_path=sys.argv[-2], sl_path=sys.argv[-1])

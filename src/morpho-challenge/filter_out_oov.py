import pandas as pd
import click
import sys

@click.command()
@click.option('--unimorph', help='Unimorph file path', required=True)
@click.option('--mc_words', help='MC relevant words path', required=True)
@click.option('--no_lemma', help='Flag to leave out lemma', is_flag=True, required=False, default=False)
def filter_oov(unimorph, mc_words, no_lemma):
    
    # open unimorph and mc
    unimorph_df = pd.read_csv(unimorph, header=None, delimiter='\t')
    unimorph_df.columns = ['word', 'lemma', 'analysis']
    mc_df = pd.read_csv(mc_words, header=None, delimiter='\t')
    mc_df.columns = ['word']

    # create set of unique words
    mc_devset_words = set(mc_df.word)
    contained_in_mc = lambda s: s in mc_devset_words

    # filter unimorph, grabbing only rows whose word appears in MC
    unimorph_mask = unimorph_df.word.apply(contained_in_mc)
    unimorph_filtered = unimorph_df[unimorph_mask]
    if no_lemma:  
        create_tsv_row = lambda row: f"{row.word}\t{row.analysis}"
    else:
        create_tsv_row = lambda row: f"{row.word}\t{row.lemma} {row.analysis}"
    output_rows = unimorph_filtered.apply(create_tsv_row, axis=1).tolist()
    output = "\n".join(output_rows)

    # finally output to stdout
    sys.stdout.write(output)
    
if __name__ == '__main__':
   filter_oov()

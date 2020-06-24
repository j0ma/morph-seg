# Adapted from https://github.com/d-ataman/lmvr

###################################################################################################################
# Duygu Ataman
#
# Example script for training a segmentation model and segmenting a corpus
#
###################################################################################################################

extension="lmvr"
lan="en"
input=brown_wordlist # input file name
dir=. # name of directory for the file
mkdir -p $dir
dictionarysize=5000  # target NMT vocabulary size (40k per Experiment 1-2a in paper)
P=10 # perplexity threshold (default 10)

### Train Morfessor Baseline for initializing the Flatcat model
echo "Training morfessor baseline..."
morfessor-train \
    -S $dir/baselinemodel.$lan.txt \
    $dir/$input 2>log.err.$lan.$extension 

## Clean lexicon for strange characters
## NOTE: this perl trick turns 

#cat $dir/baselinemodel.$lan.txt | \
    #perl -pe 's/\n/ /g' | \
    #perl -pe 's/  /\n/g' \
    #> $dir/baselinemodel.$lan.clean.txt

cp $dir/baselinemodel.$lan.txt $dir/baselinemodel.$lan.clean.txt

## Train LMVR model using the training set
echo "Training LMVR model..."
lmvr-train $dir/baselinemodel.$lan.clean.txt \
    -T $dir/$input \
    -s $dir/lmvr.${extension}.model.tar.gz \
    -m batch -p $P -d none \
    --min-shift-remainder 1 \
    --length-threshold 5 \
    --min-perplexity-length 1 \
    --max-epochs 1 \
    --lexicon-size $dictionarysize \
    -x $dir/flatcat.${extension}.lexicon.txt \
    -o $dir/$input.segmented

## Segment train, dev, and test sets using the segmentation model
echo "Segmenting using LMVR..."
lmvr-segment \
    $dir/lmvr.${extension}.model.tar.gz  \
    $dir/$input -p $P \
    --output-newlines \
    --encoding UTF-8 \
    -o $dir/$input.$extension.segmented

#cat $dir/$input.$extension.segmented | \
    #perl -pe 's/\n/ /g' | \
    #perl -pe 's/  /\n/g' > $dir/$input.$extension.segmented.sent

cp $dir/$input.$extension.segmented $dir/$input.$extension.segmented.sent

lmvr-segment \
    $dir/lmvr.${extension}.model.tar.gz  \
    $dir/dev.$lan -p $P \
    --output-newlines \
    --encoding UTF-8 \
    -o $dir/dev.$lan.$extension.segmented

#cat $dir/dev.$lan.$extension.segmented | \
    #perl -pe 's/\n/ /g' | \
    #perl -pe 's/  /\n/g' > $dir/dev.$lan.$extension.segmented.sent

cp $dir/dev.$extension.segmented $dir/dev.$extension.segmented.sent

lmvr-segment \
    $dir/lmvr.${extension}.model.tar.gz  \
    $dir/test.$lan -p $P \
    --output-newlines \
    --encoding UTF-8 \
    -o $dir/test.$lan.$extension.segmented

cp $dir/test.$extension.segmented $dir/test.$extension.segmented.sent

#cat $dir/test.$lan.$extension.segmented | \
    #perl -pe 's/\n/ /g' | \
    #perl -pe 's/  /\n/g' > $dir/test.$lan.$extension.segmented.sent


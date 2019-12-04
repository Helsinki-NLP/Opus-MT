# opus-2019-12-04.zip

* dataset: opus
* model: transformer-align
* pre-processing: normalization + SentencePiece
* download: [opus-2019-12-04.zip](https://object.pouta.csc.fi/OPUS-MT-models/de-fi/opus-2019-12-04.zip)
* test set translations: [opus-2019-12-04.test.txt](https://object.pouta.csc.fi/OPUS-MT-models/de-fi/opus-2019-12-04.test.txt)
* test set scores: [opus-2019-12-04.eval.txt](https://object.pouta.csc.fi/OPUS-MT-models/de-fi/opus-2019-12-04.eval.txt)

## Benchmarks

| testset               | BLEU  | chr-F |
|-----------------------|-------|-------|
| Tatoeba.de.fi 	| 40.1 	| 0.624 |



# goethe-2019-11-15.zip

* dataset: opus+goethe
* model: transformer
* pre-processing: normalization + tokenization + BPE
* download: [goethe-2019-11-15.zip](https://object.pouta.csc.fi/OPUS-MT-models/de-fi/goethe-2019-11-15.zip)
* info: trained on OPUS and fine-tuned for 6 epochs on data from the Goethe Institute

## Benchmarks

| testset               | BLEU  | chr-F |
|-----------------------|-------|-------|
| goethe.de.fi 	| 39.26	|	|

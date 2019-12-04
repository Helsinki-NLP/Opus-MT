# opus-2019-12-04.zip

* dataset: opus
* model: transformer
* pre-processing: normalization + tokenization + BPE
* a sentence initial language token is required in the form of `>>id<<` (id = valid target language ID)
* download: [opus-2019-12-04.zip](https://object.pouta.csc.fi/OPUS-MT-models/en-de+af+fy+nl/opus-2019-12-04.zip)
* test set translations: [opus-2019-12-04.test.txt](https://object.pouta.csc.fi/OPUS-MT-models/en-de+af+fy+nl/opus-2019-12-04.test.txt)
* test set scores: [opus-2019-12-04.eval.txt](https://object.pouta.csc.fi/OPUS-MT-models/en-de+af+fy+nl/opus-2019-12-04.eval.txt)

## Benchmarks

| testset               | BLEU  | chr-F |
|-----------------------|-------|-------|
| newssyscomb2009.en.de 	| 20.7 	| 0.510 |
| news-test2008.en.de 	| 21.0 	| 0.502 |
| newstest2009.en.de 	| 20.0 	| 0.503 |
| newstest2010.en.de 	| 22.0 	| 0.514 |
| newstest2011.en.de 	| 20.1 	| 0.491 |
| newstest2012.en.de 	| 20.6 	| 0.494 |
| newstest2013.en.de 	| 24.0 	| 0.519 |
| newstest2015-ende.en.de 	| 28.0 	| 0.551 |
| newstest2016-ende.en.de 	| 30.9 	| 0.584 |
| newstest2017-ende.en.de 	| 26.1 	| 0.542 |
| newstest2018-ende.en.de 	| 37.1 	| 0.621 |
| newstest2019-ende.en.de 	| 35.1 	| 0.597 |
| Tatoeba.en.nl 	| 44.6 	| 0.638 |


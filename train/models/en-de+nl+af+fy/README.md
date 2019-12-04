# opus-2019-12-04.zip

* dataset: opus
* model: transformer
* pre-processing: normalization + tokenization + BPE
* a sentence initial language token is required in the form of `>>id<<` (id = valid target language ID)
* download: [opus-2019-12-04.zip](https://object.pouta.csc.fi/OPUS-MT-models/en-de+nl+af+fy/opus-2019-12-04.zip)
* test set translations: [opus-2019-12-04.test.txt](https://object.pouta.csc.fi/OPUS-MT-models/en-de+nl+af+fy/opus-2019-12-04.test.txt)
* test set scores: [opus-2019-12-04.eval.txt](https://object.pouta.csc.fi/OPUS-MT-models/en-de+nl+af+fy/opus-2019-12-04.eval.txt)

## Benchmarks

| testset               | BLEU  | chr-F |
|-----------------------|-------|-------|
| newssyscomb2009.en.de 	| 20.6 	| 0.510 |
| news-test2008.en.de 	| 21.0 	| 0.501 |
| newstest2009.en.de 	| 20.1 	| 0.504 |
| newstest2010.en.de 	| 22.2 	| 0.515 |
| newstest2011.en.de 	| 20.0 	| 0.491 |
| newstest2012.en.de 	| 20.5 	| 0.493 |
| newstest2013.en.de 	| 24.3 	| 0.522 |
| newstest2015-ende.en.de 	| 28.3 	| 0.553 |
| newstest2016-ende.en.de 	| 31.1 	| 0.586 |
| newstest2017-ende.en.de 	| 25.9 	| 0.541 |
| newstest2018-ende.en.de 	| 37.5 	| 0.624 |
| newstest2019-ende.en.de 	| 35.2 	| 0.601 |
| Tatoeba.en.fy 	| 44.2 	| 0.632 |


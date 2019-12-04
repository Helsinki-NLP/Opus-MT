# opus-2019-12-04.zip

* dataset: opus
* model: transformer
* pre-processing: normalization + tokenization + BPE
* a sentence initial language token is required in the form of `>>id<<` (id = valid target language ID)
* download: [opus-2019-12-04.zip](https://object.pouta.csc.fi/OPUS-MT-models/fr-de+af+fy+nl/opus-2019-12-04.zip)
* test set translations: [opus-2019-12-04.test.txt](https://object.pouta.csc.fi/OPUS-MT-models/fr-de+af+fy+nl/opus-2019-12-04.test.txt)
* test set scores: [opus-2019-12-04.eval.txt](https://object.pouta.csc.fi/OPUS-MT-models/fr-de+af+fy+nl/opus-2019-12-04.eval.txt)

## Benchmarks

| testset               | BLEU  | chr-F |
|-----------------------|-------|-------|
| euelections_dev2019.transformer.fr 	| 24.5 	| 0.540 |
| newssyscomb2009.fr.de 	| 20.3 	| 0.502 |
| news-test2008.fr.de 	| 20.6 	| 0.503 |
| newstest2009.fr.de 	| 19.8 	| 0.496 |
| newstest2010.fr.de 	| 20.3 	| 0.504 |
| newstest2011.fr.de 	| 20.2 	| 0.491 |
| newstest2012.fr.de 	| 21.0 	| 0.493 |
| newstest2013.fr.de 	| 22.9 	| 0.509 |
| newstest2019-frde.fr.de 	| 25.6 	| 0.561 |
| Tatoeba.fr.nl 	| 46.6 	| 0.652 |


# opus-2019-12-04.zip

* dataset: opus
* model: transformer
* pre-processing: normalization + tokenization + BPE
* a sentence initial language token is required in the form of `>>id<<` (id = valid target language ID)
* download: [opus-2019-12-04.zip](https://object.pouta.csc.fi/OPUS-MT-models/en+de+nl+fy+af+da+fo+is+no+nb+nn+sv-en+de+nl+fy+af+da+fo+is+no+nb+nn+sv/opus-2019-12-04.zip)
* test set translations: [opus-2019-12-04.test.txt](https://object.pouta.csc.fi/OPUS-MT-models/en+de+nl+fy+af+da+fo+is+no+nb+nn+sv-en+de+nl+fy+af+da+fo+is+no+nb+nn+sv/opus-2019-12-04.test.txt)
* test set scores: [opus-2019-12-04.eval.txt](https://object.pouta.csc.fi/OPUS-MT-models/en+de+nl+fy+af+da+fo+is+no+nb+nn+sv-en+de+nl+fy+af+da+fo+is+no+nb+nn+sv/opus-2019-12-04.eval.txt)

## Benchmarks

| testset               | BLEU  | chr-F |
|-----------------------|-------|-------|
| newssyscomb2009.de.en 	| 19.9 	| 0.505 |
| newssyscomb2009.en.de 	| 19.9 	| 0.505 |
| news-test2008.de.en 	| 20.1 	| 0.494 |
| news-test2008.en.de 	| 20.1 	| 0.494 |
| newstest2009.de.en 	| 19.1 	| 0.496 |
| newstest2009.en.de 	| 19.1 	| 0.496 |
| newstest2010.de.en 	| 21.0 	| 0.506 |
| newstest2010.en.de 	| 21.0 	| 0.506 |
| newstest2011.de.en 	| 19.3 	| 0.486 |
| newstest2011.en.de 	| 19.3 	| 0.486 |
| newstest2012.de.en 	| 19.6 	| 0.487 |
| newstest2012.en.de 	| 19.6 	| 0.487 |
| newstest2013.de.en 	| 23.0 	| 0.512 |
| newstest2013.en.de 	| 23.0 	| 0.512 |
| newstest2014-deen.de.en 	| 26.3 	| 0.535 |
| newstest2015-ende.de.en 	| 26.6 	| 0.540 |
| newstest2015-ende.en.de 	| 26.6 	| 0.540 |
| newstest2016-ende.de.en 	| 29.1 	| 0.569 |
| newstest2016-ende.en.de 	| 29.1 	| 0.569 |
| newstest2017-ende.de.en 	| 24.5 	| 0.528 |
| newstest2017-ende.en.de 	| 24.5 	| 0.528 |
| newstest2018-ende.de.en 	| 34.9 	| 0.604 |
| newstest2018-ende.en.de 	| 34.9 	| 0.604 |
| newstest2019-deen.de.en 	| 31.3 	| 0.569 |
| newstest2019-ende.en.de 	| 32.2 	| 0.578 |
| Tatoeba.en.sv 	| 43.3 	| 0.630 |


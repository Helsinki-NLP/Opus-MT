# opus-2019-12-04.zip

* dataset: opus
* model: transformer
* pre-processing: normalization + tokenization + BPE
* a sentence initial language token is required in the form of `>>id<<` (id = valid target language ID)
* download: [opus-2019-12-04.zip](https://object.pouta.csc.fi/OPUS-MT-models/en+fr-en+fr/opus-2019-12-04.zip)
* test set translations: [opus-2019-12-04.test.txt](https://object.pouta.csc.fi/OPUS-MT-models/en+fr-en+fr/opus-2019-12-04.test.txt)
* test set scores: [opus-2019-12-04.eval.txt](https://object.pouta.csc.fi/OPUS-MT-models/en+fr-en+fr/opus-2019-12-04.eval.txt)

## Benchmarks

| testset               | BLEU  | chr-F |
|-----------------------|-------|-------|
| newsdiscussdev2015-enfr.en.fr 	| 22.2 	| 0.524 |
| newsdiscussdev2015-enfr.fr.en 	| 23.7 	| 0.524 |
| newsdiscusstest2015-enfr.en.fr 	| 24.6 	| 0.551 |
| newsdiscusstest2015-enfr.fr.en 	| 26.4 	| 0.551 |
| newssyscomb2009.en.fr 	| 21.3 	| 0.515 |
| newssyscomb2009.fr.en 	| 22.3 	| 0.515 |
| news-test2008.en.fr 	| 19.7 	| 0.492 |
| news-test2008.fr.en 	| 20.6 	| 0.492 |
| newstest2009.en.fr 	| 20.8 	| 0.511 |
| newstest2009.fr.en 	| 21.8 	| 0.511 |
| newstest2010.en.fr 	| 22.2 	| 0.521 |
| newstest2010.fr.en 	| 23.2 	| 0.521 |
| newstest2011.en.fr 	| 23.4 	| 0.533 |
| newstest2011.fr.en 	| 24.6 	| 0.533 |
| newstest2012.en.fr 	| 22.0 	| 0.514 |
| newstest2012.fr.en 	| 23.1 	| 0.514 |
| newstest2013.en.fr 	| 22.9 	| 0.514 |
| newstest2013.fr.en 	| 24.1 	| 0.514 |
| newstest2014-fren.fr.en 	| 32.4 	| 0.585 |
| Tatoeba.en.fr 	| 55.8 	| 0.688 |


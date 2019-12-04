# opus-2019-12-04.zip

* dataset: opus
* model: transformer
* pre-processing: normalization + tokenization + BPE
* a sentence initial language token is required in the form of `>>id<<` (id = valid target language ID)
* download: [opus-2019-12-04.zip](https://object.pouta.csc.fi/OPUS-MT-models/ca+es+fr+ga+it+la+oc+pt_br+pt-ca+es+fr+ga+it+la+oc+pt_br+pt/opus-2019-12-04.zip)
* test set translations: [opus-2019-12-04.test.txt](https://object.pouta.csc.fi/OPUS-MT-models/ca+es+fr+ga+it+la+oc+pt_br+pt-ca+es+fr+ga+it+la+oc+pt_br+pt/opus-2019-12-04.test.txt)
* test set scores: [opus-2019-12-04.eval.txt](https://object.pouta.csc.fi/OPUS-MT-models/ca+es+fr+ga+it+la+oc+pt_br+pt-ca+es+fr+ga+it+la+oc+pt_br+pt/opus-2019-12-04.eval.txt)

## Benchmarks

| testset               | BLEU  | chr-F |
|-----------------------|-------|-------|
| newssyscomb2009.es.fr 	| 29.6 	| 0.561 |
| newssyscomb2009.fr.es 	| 30.3 	| 0.561 |
| news-test2008.es.fr 	| 27.9 	| 0.538 |
| news-test2008.fr.es 	| 28.6 	| 0.538 |
| newstest2009.es.fr 	| 26.3 	| 0.537 |
| newstest2009.fr.es 	| 27.1 	| 0.537 |
| newstest2010.es.fr 	| 30.2 	| 0.563 |
| newstest2010.fr.es 	| 30.9 	| 0.563 |
| newstest2011.es.fr 	| 29.3 	| 0.552 |
| newstest2011.fr.es 	| 30.1 	| 0.552 |
| newstest2012.es.fr 	| 29.5 	| 0.553 |
| newstest2012.fr.es 	| 30.2 	| 0.553 |
| newstest2013.es.fr 	| 27.6 	| 0.536 |
| newstest2013.fr.es 	| 28.4 	| 0.536 |
| Tatoeba.ca.pt 	| 50.7 	| 0.659 |


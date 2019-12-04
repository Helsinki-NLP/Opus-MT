# opus-2019-12-04.zip

* dataset: opus
* model: transformer
* pre-processing: normalization + tokenization + BPE
* a sentence initial language token is required in the form of `>>id<<` (id = valid target language ID)
* download: [opus-2019-12-04.zip](https://object.pouta.csc.fi/OPUS-MT-models/en+fr-et+hu+fi/opus-2019-12-04.zip)
* test set translations: [opus-2019-12-04.test.txt](https://object.pouta.csc.fi/OPUS-MT-models/en+fr-et+hu+fi/opus-2019-12-04.test.txt)
* test set scores: [opus-2019-12-04.eval.txt](https://object.pouta.csc.fi/OPUS-MT-models/en+fr-et+hu+fi/opus-2019-12-04.eval.txt)

## Benchmarks

| testset               | BLEU  | chr-F |
|-----------------------|-------|-------|
| newsdev2015-enfi.en.fi 	| 17.6 	| 0.514 |
| newsdev2018-enet.en.et 	| 18.8 	| 0.504 |
| newstest2015-enfi.en.fi 	| 19.1 	| 0.522 |
| newstest2016-enfi.en.fi 	| 20.1 	| 0.536 |
| newstest2017-enfi.en.fi 	| 22.7 	| 0.558 |
| newstest2018-enet.en.et 	| 19.4 	| 0.512 |
| newstest2018-enfi.en.fi 	| 15.5 	| 0.489 |
| newstest2019-enfi.en.fi 	| 19.4 	| 0.507 |
| newstestB2016-enfi.en.fi 	| 16.3 	| 0.504 |
| newstestB2017-enfi.en.fi 	| 18.1 	| 0.520 |
| Tatoeba.en.fi 	| 36.7 	| 0.604 |


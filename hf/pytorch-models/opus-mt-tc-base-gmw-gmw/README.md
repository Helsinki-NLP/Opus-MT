---
language:
- af
- de
- en
- fy
- gmw
- gos
- hrx
- lb
- nds
- nl
- pdc
- yi

tags:
- translation

license: cc-by-4.0
model-index:
- name: opus-mt-tc-base-gmw-gmw
  results:
  - task:
      name: Translation afr-deu
      type: translation
      args: afr-deu
    dataset:
      name: flores101-devtest
      type: flores101
      args: afr-deu
    metrics:
       - name: BLEU
         type: bleu
         value: 21.6
  - task:
      name: Translation afr-eng
      type: translation
      args: afr-eng
    dataset:
      name: flores101-devtest
      type: flores101
      args: afr-eng
    metrics:
       - name: BLEU
         type: bleu
         value: 46.8
  - task:
      name: Translation deu-afr
      type: translation
      args: deu-afr
    dataset:
      name: flores101-devtest
      type: flores101
      args: deu-afr
    metrics:
       - name: BLEU
         type: bleu
         value: 21.4
  - task:
      name: Translation deu-eng
      type: translation
      args: deu-eng
    dataset:
      name: flores101-devtest
      type: flores101
      args: deu-eng
    metrics:
       - name: BLEU
         type: bleu
         value: 33.8
  - task:
      name: Translation eng-afr
      type: translation
      args: eng-afr
    dataset:
      name: flores101-devtest
      type: flores101
      args: eng-afr
    metrics:
       - name: BLEU
         type: bleu
         value: 33.8
  - task:
      name: Translation eng-deu
      type: translation
      args: eng-deu
    dataset:
      name: flores101-devtest
      type: flores101
      args: eng-deu
    metrics:
       - name: BLEU
         type: bleu
         value: 29.1
  - task:
      name: Translation eng-nld
      type: translation
      args: eng-nld
    dataset:
      name: flores101-devtest
      type: flores101
      args: eng-nld
    metrics:
       - name: BLEU
         type: bleu
         value: 21.0
  - task:
      name: Translation nld-eng
      type: translation
      args: nld-eng
    dataset:
      name: flores101-devtest
      type: flores101
      args: nld-eng
    metrics:
       - name: BLEU
         type: bleu
         value: 25.6
  - task:
      name: Translation deu-eng
      type: translation
      args: deu-eng
    dataset:
      name: multi30k_test_2016_flickr
      type: multi30k-2016_flickr
      args: deu-eng
    metrics:
       - name: BLEU
         type: bleu
         value: 32.2
  - task:
      name: Translation eng-deu
      type: translation
      args: eng-deu
    dataset:
      name: multi30k_test_2016_flickr
      type: multi30k-2016_flickr
      args: eng-deu
    metrics:
       - name: BLEU
         type: bleu
         value: 28.8
  - task:
      name: Translation deu-eng
      type: translation
      args: deu-eng
    dataset:
      name: multi30k_test_2017_flickr
      type: multi30k-2017_flickr
      args: deu-eng
    metrics:
       - name: BLEU
         type: bleu
         value: 32.7
  - task:
      name: Translation eng-deu
      type: translation
      args: eng-deu
    dataset:
      name: multi30k_test_2017_flickr
      type: multi30k-2017_flickr
      args: eng-deu
    metrics:
       - name: BLEU
         type: bleu
         value: 27.6
  - task:
      name: Translation deu-eng
      type: translation
      args: deu-eng
    dataset:
      name: multi30k_test_2017_mscoco
      type: multi30k-2017_mscoco
      args: deu-eng
    metrics:
       - name: BLEU
         type: bleu
         value: 25.5
  - task:
      name: Translation eng-deu
      type: translation
      args: eng-deu
    dataset:
      name: multi30k_test_2017_mscoco
      type: multi30k-2017_mscoco
      args: eng-deu
    metrics:
       - name: BLEU
         type: bleu
         value: 22.0
  - task:
      name: Translation deu-eng
      type: translation
      args: deu-eng
    dataset:
      name: multi30k_test_2018_flickr
      type: multi30k-2018_flickr
      args: deu-eng
    metrics:
       - name: BLEU
         type: bleu
         value: 30.0
  - task:
      name: Translation eng-deu
      type: translation
      args: eng-deu
    dataset:
      name: multi30k_test_2018_flickr
      type: multi30k-2018_flickr
      args: eng-deu
    metrics:
       - name: BLEU
         type: bleu
         value: 25.3
  - task:
      name: Translation deu-eng
      type: translation
      args: deu-eng
    dataset:
      name: news-test2008
      type: news-test2008
      args: deu-eng
    metrics:
       - name: BLEU
         type: bleu
         value: 23.8
  - task:
      name: Translation afr-deu
      type: translation
      args: afr-deu
    dataset:
      name: tatoeba-test-v2021-08-07
      type: tatoeba_mt
      args: afr-deu
    metrics:
       - name: BLEU
         type: bleu
         value: 48.1
  - task:
      name: Translation afr-eng
      type: translation
      args: afr-eng
    dataset:
      name: tatoeba-test-v2021-08-07
      type: tatoeba_mt
      args: afr-eng
    metrics:
       - name: BLEU
         type: bleu
         value: 58.8
  - task:
      name: Translation afr-nld
      type: translation
      args: afr-nld
    dataset:
      name: tatoeba-test-v2021-08-07
      type: tatoeba_mt
      args: afr-nld
    metrics:
       - name: BLEU
         type: bleu
         value: 54.5
  - task:
      name: Translation deu-afr
      type: translation
      args: deu-afr
    dataset:
      name: tatoeba-test-v2021-08-07
      type: tatoeba_mt
      args: deu-afr
    metrics:
       - name: BLEU
         type: bleu
         value: 52.4
  - task:
      name: Translation deu-eng
      type: translation
      args: deu-eng
    dataset:
      name: tatoeba-test-v2021-08-07
      type: tatoeba_mt
      args: deu-eng
    metrics:
       - name: BLEU
         type: bleu
         value: 42.1
  - task:
      name: Translation deu-nld
      type: translation
      args: deu-nld
    dataset:
      name: tatoeba-test-v2021-08-07
      type: tatoeba_mt
      args: deu-nld
    metrics:
       - name: BLEU
         type: bleu
         value: 48.7
  - task:
      name: Translation eng-afr
      type: translation
      args: eng-afr
    dataset:
      name: tatoeba-test-v2021-08-07
      type: tatoeba_mt
      args: eng-afr
    metrics:
       - name: BLEU
         type: bleu
         value: 56.5
  - task:
      name: Translation eng-deu
      type: translation
      args: eng-deu
    dataset:
      name: tatoeba-test-v2021-08-07
      type: tatoeba_mt
      args: eng-deu
    metrics:
       - name: BLEU
         type: bleu
         value: 35.9
  - task:
      name: Translation eng-nld
      type: translation
      args: eng-nld
    dataset:
      name: tatoeba-test-v2021-08-07
      type: tatoeba_mt
      args: eng-nld
    metrics:
       - name: BLEU
         type: bleu
         value: 48.3
  - task:
      name: Translation fry-eng
      type: translation
      args: fry-eng
    dataset:
      name: tatoeba-test-v2021-08-07
      type: tatoeba_mt
      args: fry-eng
    metrics:
       - name: BLEU
         type: bleu
         value: 32.5
  - task:
      name: Translation fry-nld
      type: translation
      args: fry-nld
    dataset:
      name: tatoeba-test-v2021-08-07
      type: tatoeba_mt
      args: fry-nld
    metrics:
       - name: BLEU
         type: bleu
         value: 43.1
  - task:
      name: Translation hrx-deu
      type: translation
      args: hrx-deu
    dataset:
      name: tatoeba-test-v2021-08-07
      type: tatoeba_mt
      args: hrx-deu
    metrics:
       - name: BLEU
         type: bleu
         value: 24.7
  - task:
      name: Translation hrx-eng
      type: translation
      args: hrx-eng
    dataset:
      name: tatoeba-test-v2021-08-07
      type: tatoeba_mt
      args: hrx-eng
    metrics:
       - name: BLEU
         type: bleu
         value: 20.4
  - task:
      name: Translation ltz-deu
      type: translation
      args: ltz-deu
    dataset:
      name: tatoeba-test-v2021-08-07
      type: tatoeba_mt
      args: ltz-deu
    metrics:
       - name: BLEU
         type: bleu
         value: 37.2
  - task:
      name: Translation ltz-eng
      type: translation
      args: ltz-eng
    dataset:
      name: tatoeba-test-v2021-08-07
      type: tatoeba_mt
      args: ltz-eng
    metrics:
       - name: BLEU
         type: bleu
         value: 32.4
  - task:
      name: Translation ltz-nld
      type: translation
      args: ltz-nld
    dataset:
      name: tatoeba-test-v2021-08-07
      type: tatoeba_mt
      args: ltz-nld
    metrics:
       - name: BLEU
         type: bleu
         value: 39.3
  - task:
      name: Translation nds-deu
      type: translation
      args: nds-deu
    dataset:
      name: tatoeba-test-v2021-08-07
      type: tatoeba_mt
      args: nds-deu
    metrics:
       - name: BLEU
         type: bleu
         value: 34.5
  - task:
      name: Translation nds-eng
      type: translation
      args: nds-eng
    dataset:
      name: tatoeba-test-v2021-08-07
      type: tatoeba_mt
      args: nds-eng
    metrics:
       - name: BLEU
         type: bleu
         value: 29.9
  - task:
      name: Translation nds-nld
      type: translation
      args: nds-nld
    dataset:
      name: tatoeba-test-v2021-08-07
      type: tatoeba_mt
      args: nds-nld
    metrics:
       - name: BLEU
         type: bleu
         value: 42.3
  - task:
      name: Translation nld-afr
      type: translation
      args: nld-afr
    dataset:
      name: tatoeba-test-v2021-08-07
      type: tatoeba_mt
      args: nld-afr
    metrics:
       - name: BLEU
         type: bleu
         value: 58.8
  - task:
      name: Translation nld-deu
      type: translation
      args: nld-deu
    dataset:
      name: tatoeba-test-v2021-08-07
      type: tatoeba_mt
      args: nld-deu
    metrics:
       - name: BLEU
         type: bleu
         value: 50.4
  - task:
      name: Translation nld-eng
      type: translation
      args: nld-eng
    dataset:
      name: tatoeba-test-v2021-08-07
      type: tatoeba_mt
      args: nld-eng
    metrics:
       - name: BLEU
         type: bleu
         value: 53.1
  - task:
      name: Translation nld-fry
      type: translation
      args: nld-fry
    dataset:
      name: tatoeba-test-v2021-08-07
      type: tatoeba_mt
      args: nld-fry
    metrics:
       - name: BLEU
         type: bleu
         value: 25.1
  - task:
      name: Translation nld-nds
      type: translation
      args: nld-nds
    dataset:
      name: tatoeba-test-v2021-08-07
      type: tatoeba_mt
      args: nld-nds
    metrics:
       - name: BLEU
         type: bleu
         value: 21.4
  - task:
      name: Translation deu-eng
      type: translation
      args: deu-eng
    dataset:
      name: newstest2009
      type: wmt-2009-news
      args: deu-eng
    metrics:
       - name: BLEU
         type: bleu
         value: 23.4
  - task:
      name: Translation deu-eng
      type: translation
      args: deu-eng
    dataset:
      name: newstest2010
      type: wmt-2010-news
      args: deu-eng
    metrics:
       - name: BLEU
         type: bleu
         value: 25.8
  - task:
      name: Translation eng-deu
      type: translation
      args: eng-deu
    dataset:
      name: newstest2010
      type: wmt-2010-news
      args: eng-deu
    metrics:
       - name: BLEU
         type: bleu
         value: 20.7
  - task:
      name: Translation deu-eng
      type: translation
      args: deu-eng
    dataset:
      name: newstest2011
      type: wmt-2011-news
      args: deu-eng
    metrics:
       - name: BLEU
         type: bleu
         value: 23.7
  - task:
      name: Translation deu-eng
      type: translation
      args: deu-eng
    dataset:
      name: newstest2012
      type: wmt-2012-news
      args: deu-eng
    metrics:
       - name: BLEU
         type: bleu
         value: 24.8
  - task:
      name: Translation deu-eng
      type: translation
      args: deu-eng
    dataset:
      name: newstest2013
      type: wmt-2013-news
      args: deu-eng
    metrics:
       - name: BLEU
         type: bleu
         value: 27.7
  - task:
      name: Translation eng-deu
      type: translation
      args: eng-deu
    dataset:
      name: newstest2013
      type: wmt-2013-news
      args: eng-deu
    metrics:
       - name: BLEU
         type: bleu
         value: 22.5
  - task:
      name: Translation deu-eng
      type: translation
      args: deu-eng
    dataset:
      name: newstest2014-deen
      type: wmt-2014-news
      args: deu-eng
    metrics:
       - name: BLEU
         type: bleu
         value: 27.3
  - task:
      name: Translation eng-deu
      type: translation
      args: eng-deu
    dataset:
      name: newstest2014-deen
      type: wmt-2014-news
      args: eng-deu
    metrics:
       - name: BLEU
         type: bleu
         value: 22.0
  - task:
      name: Translation deu-eng
      type: translation
      args: deu-eng
    dataset:
      name: newstest2015-deen
      type: wmt-2015-news
      args: deu-eng
    metrics:
       - name: BLEU
         type: bleu
         value: 28.6
  - task:
      name: Translation eng-deu
      type: translation
      args: eng-deu
    dataset:
      name: newstest2015-ende
      type: wmt-2015-news
      args: eng-deu
    metrics:
       - name: BLEU
         type: bleu
         value: 25.7
  - task:
      name: Translation deu-eng
      type: translation
      args: deu-eng
    dataset:
      name: newstest2016-deen
      type: wmt-2016-news
      args: deu-eng
    metrics:
       - name: BLEU
         type: bleu
         value: 33.3
  - task:
      name: Translation eng-deu
      type: translation
      args: eng-deu
    dataset:
      name: newstest2016-ende
      type: wmt-2016-news
      args: eng-deu
    metrics:
       - name: BLEU
         type: bleu
         value: 30.0
  - task:
      name: Translation deu-eng
      type: translation
      args: deu-eng
    dataset:
      name: newstest2017-deen
      type: wmt-2017-news
      args: deu-eng
    metrics:
       - name: BLEU
         type: bleu
         value: 29.5
  - task:
      name: Translation eng-deu
      type: translation
      args: eng-deu
    dataset:
      name: newstest2017-ende
      type: wmt-2017-news
      args: eng-deu
    metrics:
       - name: BLEU
         type: bleu
         value: 24.1
  - task:
      name: Translation deu-eng
      type: translation
      args: deu-eng
    dataset:
      name: newstest2018-deen
      type: wmt-2018-news
      args: deu-eng
    metrics:
       - name: BLEU
         type: bleu
         value: 36.1
  - task:
      name: Translation eng-deu
      type: translation
      args: eng-deu
    dataset:
      name: newstest2018-ende
      type: wmt-2018-news
      args: eng-deu
    metrics:
       - name: BLEU
         type: bleu
         value: 35.4
  - task:
      name: Translation deu-eng
      type: translation
      args: deu-eng
    dataset:
      name: newstest2019-deen
      type: wmt-2019-news
      args: deu-eng
    metrics:
       - name: BLEU
         type: bleu
         value: 32.3
  - task:
      name: Translation eng-deu
      type: translation
      args: eng-deu
    dataset:
      name: newstest2019-ende
      type: wmt-2019-news
      args: eng-deu
    metrics:
       - name: BLEU
         type: bleu
         value: 31.2
  - task:
      name: Translation deu-eng
      type: translation
      args: deu-eng
    dataset:
      name: newstest2020-deen
      type: wmt-2020-news
      args: deu-eng
    metrics:
       - name: BLEU
         type: bleu
         value: 32.0
  - task:
      name: Translation eng-deu
      type: translation
      args: eng-deu
    dataset:
      name: newstest2020-ende
      type: wmt-2020-news
      args: eng-deu
    metrics:
       - name: BLEU
         type: bleu
         value: 23.9
---
# opus-mt-tc-base-gmw-gmw

Neural machine translation model for translating from West Germanic languages (gmw) to West Germanic languages (gmw).

This model is part of the [OPUS-MT project](https://github.com/Helsinki-NLP/Opus-MT), an effort to make neural machine translation models widely available and accessible for many languages in the world. All models are originally trained using the amazing framework of [Marian NMT](https://marian-nmt.github.io/), an efficient NMT implementation written in pure C++. The models have been converted to pyTorch using the transformers library by huggingface. Training data is taken from [OPUS](https://opus.nlpl.eu/) and training pipelines use the procedures of [OPUS-MT-train](https://github.com/Helsinki-NLP/Opus-MT-train).

* Publications: [OPUS-MT – Building open translation services for the World](https://aclanthology.org/2020.eamt-1.61/) and [The Tatoeba Translation Challenge – Realistic Data Sets for Low Resource and Multilingual MT](https://aclanthology.org/2020.wmt-1.139/) (Please, cite if you use this model.)

```
@inproceedings{tiedemann-thottingal-2020-opus,
    title = "{OPUS}-{MT} {--} Building open translation services for the World",
    author = {Tiedemann, J{\"o}rg  and Thottingal, Santhosh},
    booktitle = "Proceedings of the 22nd Annual Conference of the European Association for Machine Translation",
    month = nov,
    year = "2020",
    address = "Lisboa, Portugal",
    publisher = "European Association for Machine Translation",
    url = "https://aclanthology.org/2020.eamt-1.61",
    pages = "479--480",
}

@inproceedings{tiedemann-2020-tatoeba,
    title = "The Tatoeba Translation Challenge {--} Realistic Data Sets for Low Resource and Multilingual {MT}",
    author = {Tiedemann, J{\"o}rg},
    booktitle = "Proceedings of the Fifth Conference on Machine Translation",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2020.wmt-1.139",
    pages = "1174--1182",
}
```


## Model info

* Release: 2021-02-23
* source language(s): afr deu eng fry gos hrx ltz nds nld pdc yid
* target language(s): afr deu eng fry nds nld
* valid target language labels: >>afr<< >>ang_Latn<< >>deu<< >>eng<< >>fry<< >>ltz<< >>nds<< >>nld<< >>sco<< >>yid<<
* model: transformer (base)
* data: opus ([source](https://github.com/Helsinki-NLP/Tatoeba-Challenge))
* tokenization: SentencePiece (spm32k,spm32k)
* original model: [opus-2021-02-23.zip](https://object.pouta.csc.fi/Tatoeba-MT-models/gmw-gmw/opus-2021-02-23.zip)
* more information released models: [OPUS-MT gmw-gmw README](https://github.com/Helsinki-NLP/Tatoeba-Challenge/tree/master/models/gmw-gmw/README.md)
* more information about the model: [MarianMT](https://huggingface.co/docs/transformers/model_doc/marian)

This is a multilingual translation model with multiple target languages. A sentence initial language token is required in the form of `>>id<<` (id = valid target language ID), e.g. `>>afr<<`

## Usage

A short example code:

```python
from transformers import MarianMTModel, MarianTokenizer

src_text = [
    ">>nld<< You need help.",
    ">>afr<< I love your son."
]

model_name = "pytorch-models/opus-mt-tc-base-gmw-gmw"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)
translated = model.generate(**tokenizer(src_text, return_tensors="pt", padding=True))

for t in translated:
    print( tokenizer.decode(t, skip_special_tokens=True) )

# expected output:
#     Je hebt hulp nodig.
#     Ek is lief vir jou seun.
```

You can also use OPUS-MT models with the transformers pipelines, for example:

```python
from transformers import pipeline
pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-tc-base-gmw-gmw")
print(pipe(>>nld<< You need help.))

# expected output: Je hebt hulp nodig.
```

## Benchmarks

* test set translations: [opus-2021-02-23.test.txt](https://object.pouta.csc.fi/Tatoeba-MT-models/gmw-gmw/opus-2021-02-23.test.txt)
* test set scores: [opus-2021-02-23.eval.txt](https://object.pouta.csc.fi/Tatoeba-MT-models/gmw-gmw/opus-2021-02-23.eval.txt)
* benchmark results: [benchmark_results.txt](benchmark_results.txt)
* benchmark output: [benchmark_translations.zip](benchmark_translations.zip)

| langpair | testset | chr-F | BLEU  | #sent | #words |
|----------|---------|-------|-------|-------|--------|
| afr-deu | tatoeba-test-v2021-08-07 | 0.674 | 48.1 | 1583 | 9105 |
| afr-eng | tatoeba-test-v2021-08-07 | 0.728 | 58.8 | 1374 | 9622 |
| afr-nld | tatoeba-test-v2021-08-07 | 0.711 | 54.5 | 1056 | 6710 |
| deu-afr | tatoeba-test-v2021-08-07 | 0.696 | 52.4 | 1583 | 9507 |
| deu-eng | tatoeba-test-v2021-08-07 | 0.609 | 42.1 | 17565 | 149462 |
| deu-nds | tatoeba-test-v2021-08-07 | 0.442 | 18.6 | 9999 | 76137 |
| deu-nld | tatoeba-test-v2021-08-07 | 0.672 | 48.7 | 10218 | 75235 |
| eng-afr | tatoeba-test-v2021-08-07 | 0.735 | 56.5 | 1374 | 10317 |
| eng-deu | tatoeba-test-v2021-08-07 | 0.580 | 35.9 | 17565 | 151568 |
| eng-nds | tatoeba-test-v2021-08-07 | 0.412 | 16.6 | 2500 | 18264 |
| eng-nld | tatoeba-test-v2021-08-07 | 0.663 | 48.3 | 12696 | 91796 |
| fry-eng | tatoeba-test-v2021-08-07 | 0.500 | 32.5 | 220 | 1573 |
| fry-nld | tatoeba-test-v2021-08-07 | 0.633 | 43.1 | 260 | 1854 |
| gos-nld | tatoeba-test-v2021-08-07 | 0.405 | 15.6 | 1852 | 9903 |
| hrx-deu | tatoeba-test-v2021-08-07 | 0.484 | 24.7 | 471 | 2805 |
| hrx-eng | tatoeba-test-v2021-08-07 | 0.362 | 20.4 | 221 | 1235 |
| ltz-deu | tatoeba-test-v2021-08-07 | 0.556 | 37.2 | 347 | 2208 |
| ltz-eng | tatoeba-test-v2021-08-07 | 0.485 | 32.4 | 293 | 1840 |
| ltz-nld | tatoeba-test-v2021-08-07 | 0.534 | 39.3 | 292 | 1685 |
| nds-deu | tatoeba-test-v2021-08-07 | 0.572 | 34.5 | 9999 | 74564 |
| nds-eng | tatoeba-test-v2021-08-07 | 0.493 | 29.9 | 2500 | 17589 |
| nds-nld | tatoeba-test-v2021-08-07 | 0.621 | 42.3 | 1657 | 11490 |
| nld-afr | tatoeba-test-v2021-08-07 | 0.755 | 58.8 | 1056 | 6823 |
| nld-deu | tatoeba-test-v2021-08-07 | 0.686 | 50.4 | 10218 | 74131 |
| nld-eng | tatoeba-test-v2021-08-07 | 0.690 | 53.1 | 12696 | 89978 |
| nld-fry | tatoeba-test-v2021-08-07 | 0.478 | 25.1 | 260 | 1857 |
| nld-nds | tatoeba-test-v2021-08-07 | 0.462 | 21.4 | 1657 | 11711 |
| afr-deu | flores101-devtest | 0.524 | 21.6 | 1012 | 25094 |
| afr-eng | flores101-devtest | 0.693 | 46.8 | 1012 | 24721 |
| afr-nld | flores101-devtest | 0.509 | 18.4 | 1012 | 25467 |
| deu-afr | flores101-devtest | 0.534 | 21.4 | 1012 | 25740 |
| deu-eng | flores101-devtest | 0.616 | 33.8 | 1012 | 24721 |
| deu-nld | flores101-devtest | 0.516 | 19.2 | 1012 | 25467 |
| eng-afr | flores101-devtest | 0.628 | 33.8 | 1012 | 25740 |
| eng-deu | flores101-devtest | 0.581 | 29.1 | 1012 | 25094 |
| eng-nld | flores101-devtest | 0.533 | 21.0 | 1012 | 25467 |
| ltz-afr | flores101-devtest | 0.430 | 12.9 | 1012 | 25740 |
| ltz-deu | flores101-devtest | 0.482 | 17.1 | 1012 | 25094 |
| ltz-eng | flores101-devtest | 0.468 | 18.8 | 1012 | 24721 |
| ltz-nld | flores101-devtest | 0.409 | 10.7 | 1012 | 25467 |
| nld-afr | flores101-devtest | 0.494 | 16.8 | 1012 | 25740 |
| nld-deu | flores101-devtest | 0.501 | 17.9 | 1012 | 25094 |
| nld-eng | flores101-devtest | 0.551 | 25.6 | 1012 | 24721 |
| deu-eng | multi30k_test_2016_flickr | 0.546 | 32.2 | 1000 | 12955 |
| eng-deu | multi30k_test_2016_flickr | 0.582 | 28.8 | 1000 | 12106 |
| deu-eng | multi30k_test_2017_flickr | 0.561 | 32.7 | 1000 | 11374 |
| eng-deu | multi30k_test_2017_flickr | 0.573 | 27.6 | 1000 | 10755 |
| deu-eng | multi30k_test_2017_mscoco | 0.499 | 25.5 | 461 | 5231 |
| eng-deu | multi30k_test_2017_mscoco | 0.514 | 22.0 | 461 | 5158 |
| deu-eng | multi30k_test_2018_flickr | 0.535 | 30.0 | 1071 | 14689 |
| eng-deu | multi30k_test_2018_flickr | 0.547 | 25.3 | 1071 | 13703 |
| deu-eng | newssyscomb2009 | 0.527 | 25.4 | 502 | 11818 |
| eng-deu | newssyscomb2009 | 0.504 | 19.3 | 502 | 11271 |
| deu-eng | news-test2008 | 0.518 | 23.8 | 2051 | 49380 |
| eng-deu | news-test2008 | 0.492 | 19.3 | 2051 | 47447 |
| deu-eng | newstest2009 | 0.516 | 23.4 | 2525 | 65399 |
| eng-deu | newstest2009 | 0.498 | 18.8 | 2525 | 62816 |
| deu-eng | newstest2010 | 0.546 | 25.8 | 2489 | 61711 |
| eng-deu | newstest2010 | 0.508 | 20.7 | 2489 | 61503 |
| deu-eng | newstest2011 | 0.524 | 23.7 | 3003 | 74681 |
| eng-deu | newstest2011 | 0.493 | 19.2 | 3003 | 72981 |
| deu-eng | newstest2012 | 0.532 | 24.8 | 3003 | 72812 |
| eng-deu | newstest2012 | 0.493 | 19.5 | 3003 | 72886 |
| deu-eng | newstest2013 | 0.548 | 27.7 | 3000 | 64505 |
| eng-deu | newstest2013 | 0.517 | 22.5 | 3000 | 63737 |
| deu-eng | newstest2014-deen | 0.548 | 27.3 | 3003 | 67337 |
| eng-deu | newstest2014-deen | 0.532 | 22.0 | 3003 | 62688 |
| deu-eng | newstest2015-deen | 0.553 | 28.6 | 2169 | 46443 |
| eng-deu | newstest2015-ende | 0.544 | 25.7 | 2169 | 44260 |
| deu-eng | newstest2016-deen | 0.596 | 33.3 | 2999 | 64119 |
| eng-deu | newstest2016-ende | 0.580 | 30.0 | 2999 | 62669 |
| deu-eng | newstest2017-deen | 0.561 | 29.5 | 3004 | 64399 |
| eng-deu | newstest2017-ende | 0.535 | 24.1 | 3004 | 61287 |
| deu-eng | newstest2018-deen | 0.610 | 36.1 | 2998 | 67012 |
| eng-deu | newstest2018-ende | 0.613 | 35.4 | 2998 | 64276 |
| deu-eng | newstest2019-deen | 0.582 | 32.3 | 2000 | 39227 |
| eng-deu | newstest2019-ende | 0.583 | 31.2 | 1997 | 48746 |
| deu-eng | newstest2020-deen | 0.604 | 32.0 | 785 | 38220 |
| eng-deu | newstest2020-ende | 0.542 | 23.9 | 1418 | 52383 |
| deu-eng | newstestB2020-deen | 0.598 | 31.2 | 785 | 37696 |
| eng-deu | newstestB2020-ende | 0.532 | 23.3 | 1418 | 53092 |

## Acknowledgements

The work is supported by the [European Language Grid](https://www.european-language-grid.eu/) as [pilot project 2866](https://live.european-language-grid.eu/catalogue/#/resource/projects/2866), by the [FoTran project](https://www.helsinki.fi/en/researchgroups/natural-language-understanding-with-cross-lingual-grounding), funded by the European Research Council (ERC) under the European Union’s Horizon 2020 research and innovation programme (grant agreement No 771113), and the [MeMAD project](https://memad.eu/), funded by the European Union’s Horizon 2020 Research and Innovation Programme under grant agreement No 780069. We are also grateful for the generous computational resources and IT infrastructure provided by [CSC -- IT Center for Science](https://www.csc.fi/), Finland.

## Model conversion info

* transformers version: 4.12.3
* OPUS-MT git hash: 64dc362
* port time: Sun Feb 13 00:41:02 EET 2022
* port machine: LM0-400-22516.local

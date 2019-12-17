
from apply_bpe import BPE
from mosestokenizer import MosesSentenceSplitter, MosesPunctuationNormalizer, MosesTokenizer, MosesDetokenizer
import sentencepiece as spm
import codecs


class ContentProcessor():
    def __init__(self,  srclang,
            targetlang, bpe=None,spm=None):
        self.bpe = None
        self.spm = None
        self.sentences=[]
        # load BPE model for pre-processing
        if bpe:
            # print("load BPE codes from " + bpe, flush=True)
            BPEcodes = codecs.open(bpe, encoding='utf-8')
            self.bpe = BPE(BPEcodes)

        # load SentencePiece model for pre-processing
        if spm:
            # print("load sentence piece model from " + spm, flush=True)
            self.spm = spm.SentencePieceProcessor()
            self.spm.Load(spm)

        # pre- and post-processing tools
        self.tokenizer = None
        self.detokenizer = None

        # TODO: should we have support for other sentence splitters?
        # print("start pre- and post-processing tools")
        self.sentence_splitter = MosesSentenceSplitter(srclang)
        self.normalizer = MosesPunctuationNormalizer(srclang)
        if bpe:
            self.tokenizer = MosesTokenizer(srclang)

        if bpe:
            self.detokenizer = MosesDetokenizer(targetlang)

    def preprocess(self, srctxt):
        sentSource = self.sentence_splitter([self.normalizer(srctxt)])
        self.sentences=[]
        for s in sentSource:
            if self.tokenizer:
                # print('raw sentence: ' + s, flush=True)
                tokenized = ' '.join(self.tokenizer(s))
                # print('tokenized sentence: ' + tokenized, flush=True)
                segmented = self.bpe.process_line(tokenized)
            elif self.spm:
                print('raw sentence: ' + s, flush=True)
                segmented = ' '.join(self.spm.EncodeAsPieces(s))
                # print(segmented, flush=True)
            self.sentences.append(segmented)
        return self.sentences

    def postprocess(self, recievedsentences):
        sentTranslated = []
        for index, s in enumerate(recievedsentences):
            received = s.strip().split(' ||| ')
            # print(received, flush=True)

            # undo segmentation
            if self.bpe:
                translated = received[0].replace('@@ ','')
            elif self.spm:
                translated = received[0].replace(' ','').replace('▁',' ').strip()
                # translated = sp.DecodePieces(received[0].split(' '))

            alignment = ''
            if len(received) == 2:
                alignment = received[1]
                links = alignment.split(' ')
                fixedLinks = []
                outputLength = len(received[0].split(' '))
                for link in links:
                    ids = link.split('-')
                    if ids[0] != '-1' and int(ids[0])<len(self.sentences[index]):
                        if int(ids[1])<outputLength:
                            fixedLinks.append('-'.join(ids))
                alignment = ' '.join(fixedLinks)

            if self.bpe:
                detokenized = self.detokenizer(translated.split())
            else:
                detokenized = translated

            sentTranslated.append(detokenized)
        return sentTranslated

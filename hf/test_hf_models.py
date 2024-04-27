from langcodes import *
import os
import urllib.request
from huggingface_hub import HfApi, ModelSearchArguments, ModelFilter
import transformers
from transformers import pipeline, AutoModel
import torch


testset_repo = 'https://raw.githubusercontent.com/Helsinki-NLP/OPUS-MT-testsets/master/'

def get_models():

    api = HfApi()
    model_args = ModelSearchArguments()
    all_langs = list(model_args.language)    
    filt = ModelFilter(task=model_args.pipeline_tag.Translation)
    all_models = api.list_models(filter=filt)
    # print("All translation models, including Helsinki-NLP: ",len(all_models))
    models = [model for model in all_models if model.author == 'Helsinki-NLP'] # HelsinkiNLP models
    print("Helsinki models: ",len(models))
    return(models,all_langs)



def get_testset(src,trg):

    testsets = []
    src3 = [Language.get(tag).to_alpha3() for tag in src]
    trg3 = [Language.get(tag).to_alpha3() for tag in trg]
    
    benchmarkfile = testset_repo + 'testsets.tsv'
    response = urllib.request.urlopen(benchmarkfile)
    lines = response.readlines()
    for line in lines:
        parts = line.decode('utf-8').rstrip().split("\t")
        if parts[0] != parts[1]:
            if parts[0] in src3 and parts[1] in trg3:
                srcfile = parts[6]
                trgfile = parts[7]
                return(srcfile, trgfile)
        
    return('','')


def translate(testfile, model, src, trg):
    fileurl = testset_repo + testfile
    response = urllib.request.urlopen(fileurl)
    text = response.readlines()

    try:
        if torch.cuda.is_available():
            translation_pipeline = pipeline('translation', 
                                            model=model, 
                                            src_lang=src, 
                                            tgt_lang=trg, 
                                            max_length=500,
                                            device=0)
        else:
            translation_pipeline = pipeline('translation', 
                                            model=model, 
                                            src_lang=src, 
                                            tgt_lang=trg, 
                                            max_length=500)
        # return translation_pipeline(text, batch_size=64)
        print("input: " + text[0].decode('utf-8').rstrip())
        for output in translation_pipeline(text[0].decode('utf-8').rstrip()):
            print("output: " + output['translation_text'])
    except:
        print("!!! could not translate with this model and testset")


def get_model_languages(model, langs):
    
    modelname = model.modelId
    parts = modelname.split('-')
    trg = parts[-1]
    src = parts[-2]

    valid_src = []
    valid_trg = []

    if tag_is_valid(src):
        srcdescr = Language.get(src).describe('en')
        if srcdescr['language'].find('languages') >=0:
            output = os.popen('langgroup ' + src + ' | xargs iso639 -2 -k').read()
            valid_src = output.rstrip().split(' ')
        else:
            valid_src.append(src)
            
    if tag_is_valid(trg):
        srcdescr = Language.get(trg).describe('en')
        if srcdescr['language'].find('languages') >=0:
            output = os.popen('langgroup ' + src + ' | xargs iso639 -2 -k').read()
            valid_trg = output.rstrip().split(' ')
        else:
            valid_trg.append(trg)
    
    if len(valid_src)==0:
        valid_src = [tag for tag in model.tags if tag_is_valid(tag)]

    if len(valid_trg)==0:
        valid_trg = [tag for tag in reversed(model.tags) if tag_is_valid(tag)]

    if len(valid_src)==0 and len(valid_trg)>0:
        valid_src = reversed(valid_trg)
        
    return(valid_src,valid_trg) 



print("transformers version: " + transformers.__version__)
models,langs = get_models();

for model in models:
    modelname = model.modelId
    src,trg = get_model_languages(model, langs)
    srcfile,trgfile = get_testset(src,trg)
    if srcfile != '' and trgfile != '':
        print("model: " + modelname)
        print("source text: " + srcfile)
        print("target text: " + trgfile)
        translate(srcfile,modelname,src,trg)
        fileurl = testset_repo + trgfile
        response = urllib.request.urlopen(fileurl)
        text = response.readlines()
        if len(text)>0:
            print("reference: " + text[0].decode('utf-8').rstrip())
    else:
        print("!!! no test set available for model " + modelname)
        

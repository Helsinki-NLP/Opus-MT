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



def get_testsets(src,trg):

    testsets = []
    src3 = Language.get(src).to_alpha3()
    trg3 = Language.get(trg).to_alpha3()
    
    benchmarkfile = testset_repo + 'testsets.tsv'
    print("look for testsets for " + src3 + " and " + trg3)
    response = urllib.request.urlopen(benchmarkfile)
    lines = response.readlines()
    for line in lines:
        parts = line.decode('utf-8').rstrip().split("\t")
        if parts[0] == src3 and parts[1] == trg3:
            srcfile = parts[6]
            trgfile = parts[7]
            testsets.append([srcfile, trgfile])
    return(testsets)


def translate(testfile, model, src, trg):
    fileurl = testset_repo + testfile
    response = urllib.request.urlopen(fileurl)
    text = response.readlines()
    
    translated = []
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
    # return translation_pipeline(text[0])
    print("input: " + text[0].decode('utf-8').rstrip())
    for output in translation_pipeline(text[0].decode('utf-8').rstrip()):
        print("output: " + output['translation_text'])



print("transformers version: " + transformers.__version__)
models,langs = get_models();

for model in models:
    modelname = model.modelId
    parts = modelname.split('-')
    trg = parts[-1]
    src = parts[-2]

    if not tag_is_valid(src) or not tag_is_valid(trg):
        model_langs = [tag for tag in model.tags if tag in langs]
        if len(model_langs) > 0:
            if not tag_is_valid(src):
                src = model_langs[0]
            if not tag_is_valid(trg):
                trg = model_langs[-1]
    
    if tag_is_valid(src) and tag_is_valid(trg):
        # print(modelname + "\t" + src + "\t" + trg)
        testsets = get_testsets(src,trg)
        if len(testsets)>0:
            print("model: " + modelname)
            print("source text: " + testsets[0][0])
            print("target text: " + testsets[0][1])
            translate(testsets[0][0],modelname,src,trg)
            fileurl = testset_repo + testsets[0][1]
            response = urllib.request.urlopen(fileurl)
            text = response.readlines()
            print("reference: " + text[0].decode('utf-8').rstrip())
        else:
            print("!!! no test set available for model " + modelname + " and " + src + "-" + trg)
    else:
        print("!!! no valid languages found for model " + modelname)
        

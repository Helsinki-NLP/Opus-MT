#!/usr/bin/env python

# 16-Aug-2023 Joachim Schurig
#
# This code is in the public domain. If you need a license, take the
# MIT license.
#
# Many Opus language models come with an unusual configuration:
# they use spms for source fragmentation, but the language model
# then uses different index values for inference as those in the spms.
#
# Those index values are stored in a vocab.yaml file.
#
# The original proposed workflow is to run sentencepiece first with the
# original spm, then call marian with the split subwords, marian will
# then use the indexes for these from the yaml, and in the
# end a script will replace all word starts with spaces.
#
# This python script creates a combined source/target spm which reads
# the original spms, but changes all indexes in a way that it resembles
# what marian sees when using the vocab.yaml.
#
# After creating the regenerated spm, no source or target conversions are
# needed. Directly use the marian decoder with -v new_spm new_spm (same
# spm for source and target).
#
# This script would notice and warn about index collisions.

import argparse, tempfile, yaml
import sentencepiece_model_pb2 as sp_model

# parse arguments
def GetArgs():
	parser = argparse.ArgumentParser()
	parser.add_argument("-v", "--vocab" , help="vocab yaml file", required=True)
	parser.add_argument("-s", "--source", help="source spm file", required=True)
	parser.add_argument("-t", "--target", help="target spm file", required=True)
	parser.add_argument("-o", "--out"   , help="output spm file", required=True)
	return parser.parse_args()

# returns the fixed yaml
def GetFixedVocabFile(filename):
	fixed_vocab_file = tempfile.TemporaryFile(mode='w+')

	# fix the yaml file by putting double quotes around all keys
	# except those that already contain double quotes, or end in
	# a backslash (our main purpose is to repair ints and floats
	# into being strings)

	with open(args.vocab, 'r') as file:
		ids_seen = {} # map to store only last of multiple dupes on the ID value (probably not needed)
		for line in file:
			if len(line) != 0:
				pos = line.rfind(': ')
				if pos != -1:
					id = int(line[pos+2:len(line)-1]) # get rid of the lf ..
					piece = line[:pos]
					qpos = piece.find('"')
					if qpos == -1:
						if piece[0] != '\\' and piece[len(piece)-1] != '\\':
							piece = '"{}"'.format(piece)
					if ids_seen.get(id) is not None:
						print('duplicate vocab id: {}'.format(id))
					ids_seen[id] = piece

		for id, piece in ids_seen.items():
			fixed_vocab_file.write('{}: {}\n'.format(piece, id))

	fixed_vocab_file.seek(0)
	return yaml.safe_load(fixed_vocab_file)

def LoadSPM(filename):
	spm = sp_model.ModelProto()
	spm.ParseFromString(open(filename, 'rb').read())
	return spm

def AddPieces(label, vocab, spm, npieces):
	# read all pieces and map them into the new array
	# at positions looked up in the vocab file
	for p in spm.pieces:
		key = str(p.piece)
		id = vocab.get(key)
		if id is not None:
			if npieces[id] is not None:
				if npieces[id].piece != key:
					# this should not happen
					print('duplicate {} id: {}, old key: {}, new key: {}'.format(label, id, npieces[id].piece, key))
			else:
				npieces[id] = p
		else:
			# this happens for a few, and normally does not harm
			print('{} key {} not found'.format(label, key))

def RecreateSPMWithVocab(label, size, vocab, spm):
	# create an empty list with room for all pieces
	npieces = [None] * size
	AddPieces(label, vocab, spm, npieces)
	return npieces

def CreateUnused(id):
	# create a new sentence piece object
	sp       = sp_model.ModelProto.SentencePiece()
	sp.type  = sp_model.ModelProto.SentencePiece.Type.UNUSED
	sp.piece = "!<.{}".format(id)
	sp.score = 0.0
	return sp

def FillGaps(npieces):
	count = 0
	ect = 0
	for p in npieces:
		if p is None:
			npieces[count] = CreateUnused(count)
			ect += 1
		count += 1
	print ('had {} undefined pieces out of {}'.format(ect, count))

def WriteReordered(name, spm, npieces):
	# replace the old pieces with spieces
	del spm.pieces[:]
	spm.pieces.extend(npieces)
	# and write the combined sentence piece model into the output file
	with open(name, 'wb') as f:
		f.write(spm.SerializeToString())
	print ('created spm {} with {} sentence pieces for Marian NMT'.format(name, len(spm.pieces)))

# main
args  = GetArgs()
vocab = GetFixedVocabFile(args.vocab)
src   = LoadSPM(args.source)
trg   = LoadSPM(args.target)

ssize = len(src.pieces)
print("source size: ", ssize)
tsize = len(trg.pieces)
print("target size: ", tsize)

new_pieces = RecreateSPMWithVocab("source", ssize + tsize, vocab, src)
AddPieces("target", vocab, trg, new_pieces)
FillGaps(new_pieces)
WriteReordered(args.out, src, new_pieces)

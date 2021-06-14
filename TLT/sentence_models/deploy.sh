#!/bin/bash

input_file=##PROVIDE## #Provide the name of the initial training data csv file Try: "imperative_sentences_training_data.csv"
training_data="data/training_data.csv"

# ###########################################################

#run dataset through rscript to ensure there are no duplicates=
Rscript get_training_data.R -i $input_file

#run sentence embeddings
python sentence_embedding.py -i $training_data

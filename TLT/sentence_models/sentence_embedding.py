import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns
import sys, getopt, csv



module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/3" #@param ["https://tfhub.dev/google/universal-sentence-encoder/2", "https://tfhub.dev/google/universal-sentence-encoder-large/3"]

embed = hub.Module(module_url)

# get the directory where the wav files are from the user
def getArgs(argv):
    #get args wav path, chunk size default to 30secs
    out_file=''
    try:
        opts, args = getopt.getopt(argv,"hi:",["in_file"])
    except getopt.GetoptError:
        print('usage: sentence_embedding.py -i <in_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('usage: sentence_embedding.py -i <in_file>')
            sys.exit()
        elif opt in ("-i", "--in_file"):
            in_file=arg
    #now we return the variables to be passed forward
    return (in_file)

def plot_similarity(labels, features, rotation):
    corr = np.inner(features, features)
    sns.set(font_scale=1.2)
    g = sns.heatmap(
                    corr,
                    xticklabels=labels,
                    yticklabels=labels,
                    vmin=0,
                    vmax=1,
                    cmap="YlOrRd")
    g.set_xticklabels(labels, rotation=rotation)
    g.set_title("Semantic Textual Similarity")


def run_and_plot(session_, input_tensor_, messages_, encoding_tensor):
    message_embeddings_ = session_.run(encoding_tensor, feed_dict={input_tensor_: messages_})
    plot_similarity(messages_, message_embeddings_, 90)


def main():

    argv = sys.argv[1:]
    (in_file) = getArgs(argv)
    # read in CSV on pandas
    data = pd.read_csv(in_file)
    # get the text into its own object
    text = list(data['text'])
    # modifications for speech tf hub thing
    similarity_input_placeholder = tf.placeholder(tf.string,  shape=(None))
    similarity_message_encodings = embed(similarity_input_placeholder)

    #put the text from the DF in it's own series

    out_file= "%s_emb.csv" % (in_file)
    with tf.Session() as session:
      session.run(tf.global_variables_initializer())
      session.run(tf.tables_initializer())
      similarity_message_encodings = session.run(embed(text))

      for i, similarity_message_encoding in enumerate(np.array(similarity_message_encodings).tolist()):
        with open(out_file , "a") as outfile:
            # write some code to add the text in the first row

            writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(similarity_message_encoding)
    string="dim"
    header=[string+str(i) for i in range(512)]
    df_emb= pd.read_csv(out_file,names = header)
    df_out = pd.concat([data, df_emb], axis=1)
    df_out.to_csv(in_file,index=False)
    os.remove(out_file)
if __name__ == '__main__':
    main()

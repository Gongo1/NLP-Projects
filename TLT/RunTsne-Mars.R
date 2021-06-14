library(Rtsne)
library(data.table)
library(optparse)
library(RColorBrewer)
library(stringi)
library(caret)
library(ggplot2)
library(RXKCD)
library(tm)
library(wordcloud)
library(RColorBrewer)
setwd("~/Desktop/TLT/text/")

#Create a cosine similarity matrix 
#send Drew plot and explain what is happening 

# read in data (Embeddings & Sentences)

sentences <- read.csv("Pet_embed.csv", header = TRUE)
#Get rid of first Col
sentences <- sentences[,-1]
#Clean up data a bit:

#Take only dim columns for furthe analysis
universal <- sentences[-c(1)]
#word_embed1 = word_embed[,-1, drop = FALSE]

#Remove Duplicates/Check For duplicates
#universal_clean <- universal[-c(which(duplicated(universal) == TRUE)),]

remove_index <- which(duplicated(universal) == TRUE)

universal <- universal[-remove_index,]

tsne <- Rtsne(universal,perplexity = 15, stop_lying_iter = 200)
sent_tsne<-data.frame(tsne$Y)
setnames(sent_tsne,c("X1","X2"),c("tsne_1","tsne_2"))

#Add labels for color coding purposes
#Option to add further columns of text to dataframe for further analyis
pet <- read.csv("pet_sentiment_sentences.csv")
#If duplicates then remove index's as well
pet <- pet[-remove_index,]
pet <- pet[c(1:4892),]
pet_type <- pet$animal
food_tag <- pet$tag
new_tsne <- cbind(sent_tsne, pet_type, food_tag)

temp <- cbind(universal, sent_tsne)
tsne$stop_lying_iter

#test
#test <- as.data.frame(t(word_embed$X0))

#No Color
set.seed("123")

#Food Descriptors 
p <- ggplot(new_tsne, aes(x=tsne_1,y=tsne_2)) +
  geom_point() +
  xlim(-150, 150) +
  ggtitle("Pet Descriptors - Sentence Similarity")  

p + geom_jitter(width = -3 , height = -3,aes(colour = ))

#Animal Type
p <- ggplot(new_tsne, aes(x=tsne_1,y=tsne_2)) +
  geom_point() +
  xlim(-150, 150) +
  ylab("Weight-TSNE1")+
  xlab("WEIGHT-TSNE2") +
  ggtitle("Pet-Parent Sentence Similarity")  

p + geom_jitter(width = -3 , height = -3,aes(colour = pet_type))


#Color by Code 
#Color by major, school, etc... procedural vs decaritive 
q <- ggplot(new_tsne, aes(x=new_tsne$tsne_1,y=new_tsne$tsne_2,color=new_tsne$new_col, 
                          label = Course_Title)) +
  geom_point() +
  theme(legend.position = c(0.3, 0.95)) +
  ggtitle("TSNE on Classroom Descriptions")  +
  geom_text(aes(label = Course_Title))
q



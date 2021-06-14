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
setwd("~/Desktop/cramless/data/text_data/")

#Create a cosine similarity matrix 
#send Drew plot and explain what is happening 

# read in data (Embeddings & Sentences)

sentences <- read.csv("USE.csv", header = FALSE)
sentences <- sentences[,-1]
#Clean up data a bit:

#Fix Title Column
names(sentences)[names(sentences) == 'V2'] <- 'Course_Title'
sentences$Course_Title <-substr(sentences[,1], 7, 100)

#Fixed Course Names
names(sentences)[names(sentences) == 'V3'] <- 'Course_Code'
sentences$Course_Code <-substr(sentences[,2], 14, 23)

#Fix Credits Column
names(sentences)[names(sentences) == 'V4'] <- 'Credits'
sentences$Credits <-substr(sentences[,3], 10, 23)

#Fix Description Col. 
names(sentences)[names(sentences) == 'V5'] <- 'Descriptions'
sentences$Descriptions <-substr(sentences[,4], 14, 1000000)

#Take only dim columns for furthe analysis
universal <- sentences[-c(1:4)]
#word_embed1 = word_embed[,-1, drop = FALSE]

tsne <- Rtsne(universal,perplexity = 1, stop_lying_iter = 200)
sent_tsne<-data.frame(tsne$Y)
setnames(sent_tsne,c("X1","X2"),c("tsne_1","tsne_2"))
#Add labels for color coding purposes
#new_col <- c(rep("IST",5), rep("SRA",2))

Course_Title <- sentences$Course_Code
Course_credits <- sentences$Credits
new_tsne <- cbind(sent_tsne, Course_Title, Course_credits)
temp <- cbind(universal, sent_tsne)

tsne$stop_lying_iter

#test
#test <- as.data.frame(t(word_embed$X0))

#No Color
set.seed("123")
p <- ggplot(new_tsne, aes(x=new_tsne$tsne_1,y=new_tsne$tsne_2, 
                          label = Course_Title)) +
 geom_point() +
  xlim(-150, 150) +
  ggtitle("TSNE on NSA Certifite by class")  +
  geom_text(aes(label = Course_Title), hjust = 0, vjust = 0)  
  
p + geom_jitter(width = -3 , height = -3,aes(colour = Course_credits))


#Color by Code 
#Color by major, school, etc... procedural vs decaritive 
q <- ggplot(new_tsne, aes(x=new_tsne$tsne_1,y=new_tsne$tsne_2,color=new_tsne$new_col, 
                          label = Course_Title)) +
  geom_point() +
  theme(legend.position = c(0.3, 0.95)) +
  ggtitle("TSNE on Classroom Descriptions")  +
  geom_text(aes(label = Course_Title))
q



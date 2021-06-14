library("optparse")
library("data.table")

#setwd("..")
training_data <- fread("audio_analysis_demo/sentence_models/data/imperative_sentences_training_data.csv", header = TRUE)
processed_audio <- fread("audio_analysis_demo/project/volume/data/processed.csv", header = TRUE)

#Deleting all old negative examples
training_data <- subset(training_data, label == 1)

#Getting negative examples from processed.csv
length_processed_audio <- nrow(processed_audio$text)
x <- nrow(training_data)
rand_sampl <- sample(length_processed_audio, x)
random_text <- processed_audio$text[rand_sampl]
neg_ex <- c(rep(0,x))
negative_data_df <- cbind(random_text, neg_ex)

#New training dataset
new_training_data <- rbind(training_data, negative_data_df, use.names=FALSE)

fwrite(new_training_data, "audio_analysis_demo/sentence_models/data/training_data.csv")
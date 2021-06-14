library(optparse)
library(data.table)

validation_data <- fread("audio_analysis_demo/sentence_models/data/imperative_validation_data.csv", header = TRUE)
processed_audio <- fread("audio_analysis_demo/project/volume/data/processed.csv", header = TRUE)

#Getting negative examples from processed.csv
length_processed_audio <- nrow(processed_audio)
length_validation <- nrow(validation_data)
rand_sampl <- sample(length_processed_audio, length_validation)
random_text <- processed_audio$text[rand_sampl]
neg_ex <- c(rep(0,length_validation))
negative_data_df <- cbind(random_text, neg_ex)


new_validation_data <- rbind(validation_data, negative_data_df, use.names=FALSE)
fwrite(new_validation_data, "audio_analysis_demo/sentence_models/data/validation_data.csv")

View(new_validation_data)

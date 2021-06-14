#Install Packages
#install.packages("optparse")
#install.packages("contrib.url")

#Import Packages
library("optparse")
library("data.table")
#library("contrib.url")

#Get Arguments from Command Line
option_list = list(
  make_option(c("-i", "--input"), type="character", default=NULL,
              help="path to directory with .cvs files", metavar="character")
);

opt_parser <- OptionParser(option_list = option_list)
opt <- parse_args(opt_parser)
# print(opt$input)

#Clean up dataset
input_data <- fread(opt$input, header = TRUE)
training_data <- unique(input_data)
# print(training_data)

fwrite(training_data, "data/training_data.csv")

# This script generates a list of all possible media on the flights
library(tidyverse)
library(readr)

# Read in unique media values
SIA_media_content_entire_yr <- read_csv("data/media_load/SIA_media_content_entire_yr.csv")

# Filter only for the loads present in the tail data
load_num <- c("AAK_1218_v3", "AAK_1018_v3", "AAK_1118_v4", "AAK_0119_v3", "AAK_0219_v7")
load_vector <- data.frame(cbind(load_num, c(1,2,3,4,5)))

# For appending cycle number
colnames(load_vector) <- c("data_source", "cycle_no")
content_filter <- c("movie",  "tvepisode")

SIA_media_content_5_months <- SIA_media_content_entire_yr %>%
  filter(data_source %in% load_num) %>%
  filter(contenttype %in% content_filter) %>%
  left_join(load_vector) %>%
  select(-duration, -MID) %>%
  unique()

SIA_id <- SIA_media_content_5_months %>%
  group_by(uniqueID, data_source) %>%
  summarize(n())

SIA_sum <- SIA_media_content_5_months %>%
  group_by(cycle_no) %>%
  summarize(n())

#Writes the summary table
write.csv(SIA_sum, "output/cycle_table.csv")

# Data sorting
sia_summary <- SIA_media_content_5_months %>%
  group_by(uniqueID, cycle_no) %>%
  summarize(count = n()) %>%
  arrange(desc(count)) %>%
  filter(count > 1)

# Check for and remove duplicate values
SIA_content_5mo_nondup <- SIA_media_content_5_months %>%
  filter(!uniqueID %in% sia_summary$uniqueID)

SIA_content_5mo_dup <- SIA_media_content_5_months %>%
  filter(uniqueID %in% sia_summary$uniqueID) %>%
  filter(midType != "videoAggregate") %>%
  unique()

SIA_content_5mo_final <- bind_rows(SIA_content_5mo_nondup, SIA_content_5mo_dup)

# Country name standardization
x <- str_replace_all(SIA_content_5mo_final$countryOrigin, "\\)","")
y <- unlist(str_split_fixed(x,"\\(",n=3))
z <- matrix(ifelse(str_length(y)==3,y,""), ncol = 3, byrow=FALSE)
s <- paste(z[,1],z[,2],z[,3],sep="")
s[s==""] <- NA

SIA_content_5mo_final$countryOrigin <- s

write.csv(SIA_content_5mo_final, "output/SIA_content_5mo_final.csv")
# This script generates a master media key file based on the flight usage data.

# Required packages
library(readr)
library(tidyverse)
library(stringi)
library(qdapTools)

# Get all possible media keys from flights
sia_media_usage_master <- 
  read_csv("data/media_usage/sia_media_usage_master.csv")

media_listing <- sia_media_usage_master %>%
  select(media_key) %>%
  unique()

rm(sia_media_usage_master)

# Get all media data loaded on an airplane and match to a uniqueID.
SIA_media_data_entire_yr <- 
  read_csv("data/media_load/SIA_media_data_entire_yr.csv")

media_key_lookup <- SIA_media_data_entire_yr %>%
  select(media_key, media_unique_id) %>%
  unique()

airline_media <- left_join(media_listing, media_key_lookup) %>%
  rename(uniqueID = media_unique_id)

rm(SIA_media_data_entire_yr, media_key_lookup, media_listing)

#Load media content data
SIA_media_content_entire_yr <- 
  read_csv("data/media_load/SIA_media_content_entire_yr.csv")

media_attributes <- SIA_media_content_entire_yr %>%
  select(uniqueID, midType, title, contenttype) %>%
  filter(midType == "video") %>%
  unique()

airline_media2 <- left_join(airline_media, media_attributes)

rm(airline_media)

# Remove duplicates from airline media info
airline_key_count <- airline_media2 %>%
  select(media_key) %>%
  group_by(media_key) %>%
  summarise(count = n())

airline_dups <- left_join(airline_media2, airline_key_count) %>%
  filter(count > 1) %>%
  filter(contenttype != "base_movie") %>%
  filter(contenttype != "promo") %>%
  filter(contenttype != "base_tvepisode") %>%
  filter(title != "Adult/Language/Aircraft Issues - ENG/MAN") %>%
  filter(title != "Passenger Health Advisory Taipei") %>%
  select(-count)

airline_final <- left_join(airline_media2, airline_key_count) %>%
  filter(count == 1) %>%
  bind_rows(airline_dups)

rm(airline_dups,airline_key_count,airline_media2)

#Split into movie, tv, and other files
movie_id <- airline_final %>%
  filter(contenttype %in% c("movie","base_movie"))

tv_id <- airline_final %>%
  filter(contenttype %in% c("base_tvepisode", "tvepisode"))

other_id <- airline_final %>%
  filter(contenttype %in% c("advert","trailer","graphic",NA))

# Generate movie file
media_info <- SIA_media_content_entire_yr %>%
  filter(contenttype %in% c("movie","base_movie")) %>%
  select(year, genre, ratingDes, uniqueID, countryOrigin, peopleScore, criticScore, omDb_imdbID, omDb_Awards) %>%
  unique()

movie_class_final <- left_join(movie_id, media_info) %>%
  select(-count)

movie_counter <- movie_class_final %>%
  select(media_key) %>%
  group_by(media_key) %>%
  summarize(count = n())

movie_dup <- left_join(movie_class_final, movie_counter) %>%
  filter(count >1)

dim(movie_dup)[1]  # This should be 0

cast_info_movie <- SIA_media_content_entire_yr %>%
  filter(contenttype %in% c("movie","base_movie")) %>%
  select(uniqueID, cast) %>%
  unique()

cast_info_movie <- cast_info_movie[-which(duplicated(cast_info_movie$uniqueID)),]

movie_class_final <- left_join(movie_class_final, cast_info_movie)

# Generate TV file
media_info_tv <- SIA_media_content_entire_yr %>%
  filter(contenttype %in% c("base_tvepisode", "tvepisode")) %>%
  select(year, genre, ratingDes, uniqueID, countryOrigin, peopleScore, criticScore, omDb_imdbID, agg_title, title) %>%
  filter(agg_title != title) %>%
  unique()

tv_class_final <- left_join(tv_id, media_info_tv) %>%
  select(-count)

tv_counter <- tv_class_final %>%
  select(media_key) %>%
  group_by(media_key) %>%
  summarize(count = n())

tv_dup <- left_join(tv_class_final, tv_counter) %>%
  filter(count > 1) %>%
  filter(genre != "Food Culture") %>%
  filter(countryOrigin != "China(CHN)")
  
tv_final <- left_join(tv_class_final, tv_counter) %>%
  filter(count == 1) %>%
  bind_rows(tv_dup)

cast_info_tv <- SIA_media_content_entire_yr %>%
  filter(contenttype %in% c("base_tvepisode", "tvepisode")) %>%
  select(uniqueID, cast) %>%
  unique()

cast_info_tv <- cast_info_tv[-which(duplicated(cast_info_tv$uniqueID)),]

tv_final <- left_join(tv_final, cast_info_tv)

rm(airline_final, cast_info_movie, cast_info_tv, media_attributes, 
   media_info, media_info_tv, movie_counter, movie_dup, movie_id, 
   SIA_media_content_entire_yr, tv_counter, tv_dup, tv_class_final, tv_id)

# Part 2 - Advanced data cleansing: Country of Origin standardization
media_match <- bind_rows(movie_class_final, other_id, tv_final) %>%
  select(-count)

x <- str_replace_all(media_match$countryOrigin, "\\)","")
y <- unlist(str_split_fixed(x,"\\(",n=3))
z <- matrix(ifelse(str_length(y)==3,y,""), ncol = 3, byrow=FALSE)
s <- paste(z[,1],z[,2],z[,3],sep="")
s[s==""] <- NA
media_match$countryOrigin <- s

unique(media_match$countryOrigin)

nom_idx <- grep("(nominat)",media_match$omDb_Awards)
win_idx <- grep("(win)",media_match$omDb_Awards)

media_match$nom_idx <- 0
media_match$win_idx <- 0

media_match$nom_idx[nom_idx] <- 1
media_match$win_idx[win_idx] <- 1


# Part 3 - Advanced data cleansing: Actor Feature Engineering
actors <- media_match$cast

#<-----Note: Replace this with a "get actors" script ------>
top_actors <- read_csv("data/other/top_actors.csv", 
  col_types = cols_only(Name = col_guess()))

a_list <- rep(NA, length(actors))

for(i in 1:length(actors)){
  actor_break <- trimws(unlist(str_split(actors[i], ",")))
  a_list[i] <- sum(actor_break %in% top_actors$Name)
  }

media_match$a_list_qty <- a_list

# Relabeling some media
media_match$contenttype[media_match$contenttype=="base_movie"] <- "movie"
media_match$contenttype[media_match$contenttype=="base_tvepisode"] <- "tvepisode"

# Write to a "media match" file that can be merged with the usage file.
write.csv(media_match, "output/media_match.csv", row.names = FALSE)
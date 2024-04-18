library(readr)
library(tidyverse)

# Read in media_match data
media_match <- read_csv("output/media_match.csv")

# Read in tail data
sia_media_usage_master <- read_csv("data/media_usage/sia_media_usage_master.csv")

#Join the two files
media_use_master <- left_join(sia_media_usage_master, media_match)

# Find distinct airport codes
airport_codes_arr <- unique(sia_media_usage_master$arrival_airport_icao_code)
airport_codes_dep <- unique(sia_media_usage_master$departure_airport_icao_code)

airport_code_final <- unique(c(airport_codes_arr, airport_codes_dep))

# Use open airports to generate a master list of airport codes
country_codes <- read_csv("http://ourairports.com/data/countries.csv") %>%
  select(code, name)

airport_codes <- read_csv("http://ourairports.com/data/airports.csv") %>%
  select(ident, name, iso_country)

airport_data <- left_join(airport_codes, country_codes, by=c("iso_country"="code")) %>%
  rename(airport_name = name.x, country_name = name.y) %>%
  filter(ident %in% airport_code_final)

# Join with the master file
media_use_master_air <- left_join(media_use_master, airport_data, 
                                  by=c("arrival_airport_icao_code" = "ident")) %>%
  rename(arr_airport_name = airport_name, 
         arr_airport_iso_country = iso_country,
         arr_airport_country_name = country_name)

media_use_master_air <- left_join(media_use_master_air, airport_data, 
                                  by=c("departure_airport_icao_code" = "ident")) %>%
  rename(dep_airport_name = airport_name, 
         dep_airport_iso_country = iso_country,
         dep_airport_country_name = country_name)

# Filter out non-movie/tv shows
media_use_master_air_filtered <- media_use_master_air %>%
  filter(contenttype %in% c("movie", "tvepisode"))

n <- dim(media_use_master)[1]

# Variable selection
media_use_master_f_compact <- media_use_master_air_filtered %>%
  select(-usage_type_name, -omDb_Awards, -cast, -omDb_imdbID) %>%
  arrange(arr_airport_iso_country,dep_airport_iso_country) %>%
  mutate(routeid = paste(arrival_airport_icao_code,departure_airport_icao_code, sep="_"))

# Write to output
write.csv(media_use_master_f_compact, "output/media_use_master_f_ttl.csv", row.names = FALSE)
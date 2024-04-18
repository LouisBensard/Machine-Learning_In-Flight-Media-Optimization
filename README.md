# Media Content Optimization for In-Flight Entertainment 🛫📊

## Overview 🌎 
This repository hosts our project on optimizing in-flight media content, aimed at enhancing passenger satisfaction while minimizing content costs. Developed in collaboration with Panasonic Aviation Corporation and Black Swan Data, this project utilizes advanced statistical models to predict and optimize media selection on flights.

## Table of Contents 📑
- [Project Introduction](#project-introduction-)
- [Data Collection and Processing](#data-collection-and-processing-)
- [Methodology](#methodology-)
- [Results and Insights](#results-and-insights-)
- [Future Work](#future-work-)
- [Team](#team)
- [Contact](#contact-)

## Project Introduction 📖
Our goal was to provide airlines with actionable recommendations for their in-flight entertainment offerings, predicting which media items are preferred by passengers and suggesting optimal changes to the media load. This includes both recommendations for media to remove (Recommendation I) and suggestions for new media to add (Recommendation II).

[![Overview of Media Optimization](/images/World_Map.png)](#)

## Data Collection and Processing 📊
We analyzed five months of historical flight data from Singapore Airlines, focusing on various aspects such as media usage and flight details. The data was thoroughly cleansed and prepared for analysis, involving steps like dimension reduction, data manipulation, and missing data imputation.

- **Flight Data Example**: Includes flight number, departure airport, seat number, departure date, and media ID.
- **Media Data Example**: Details media titles, types, release years, genres, and viewer scores.

[![Data Snapshot](/images/Data_Extract.png)](#)

[![Data Snapshot](/images/Aggregation.png)](#)

### Feature Engineering 
We enhanced our dataset by introducing features such as seat class, release year category, A-list actors, and price tags, significantly improving the predictive power of our models.

- **Key Features**:
    - A-List Actors: Number of top-grossing actors in a title.
    - Proportion Viewed and Used: Metrics calculated to gauge viewer engagement.

[![Feature Engineering](/images/Feature_Engineering.png)](#)

## Methodology 🔍
Our approach combined **Generalized Linear Modeling (GLM)** with **k-fold Cross-Validation** to predict the proportion of views for each media item. We focused on:
- **Feature Engineering**: Introduced new features like A-list actors, release year categories, and viewer preferences.
- **Model Optimization**: Utilized GLM for prediction with a logit link function due to the binary nature of our response variable (proportion views).

[![Data Snapshot](/images/glm.png)](#)

[![Data Snapshot](/images/Cross_Validation.png)](#)

### Advanced Techniques
- **Data Augmentation**: Enhanced media data using external datasets to fill missing values.
- **Predictive Modeling**: Employed GLM from the statemodel library in Python to forecast media performance on future flights.

## Results and Insights 📈
The analysis led to the development of a media recommendation system that accurately identifies underperforming media and suggests additions to enhance viewer satisfaction. Key insights include:
- A minority of media titles are watched by a majority of passengers, aligning with Pareto's Principle.
- Strategic recommendations are provided to manage media content effectively, balancing cost and satisfaction.

[![Prediction vs Baseline](/images/Result1_Scenario1.png)](#)

[![In-Flight Media Selection](/images/Result2_Scenario1.png)](#)

[![Improvement over baseline](/images/Result3_Scenario1.png)](#)

## Future Work 🔮
- **Cost-Benefit Analysis**: Quantify the financial impact of each media view to refine investment strategies.
- **Dynamic Media Loading**: Suggest implementing software updates to allow for dynamic media loading based on specific flight routes or passenger demographics.
- **Seasonal and Day-of-Week Trends**: Explore how media preferences change over seasons and days of the week to further tailor content.

## Team 🤝
- Louis Bensard
- Roxxanne Hobart
- Kevin Mori
- Mydoris Soto
- WanYi Dai
- Ping Zhao
- Nuno Malta

## Contact 📬
For more information on this project, please reach out at [Your Email](mailto:louisbenss@gmail.com).

Project Link: [https://github.com/LouisBensard/ML-Project01_InFlight-Media-Optimization.git](\https://github.com/LouisBensard/ML-Project01_InFlight-Media-Optimization.git)

---

# Media Optimization for In-Flight Entertainment 🛫📊

## Overview 🌎 
This repository hosts our project on optimizing in-flight media content, aimed at enhancing passenger satisfaction while minimizing content costs. Developed in collaboration with Panasonic Aviation Corporation and Black Swan Data, this project utilizes advanced statistical models to predict and optimize media selection on flights.

Read our detailed paper outlining the research and results here: [In-Flight Media Content Optimization Paper](/Final_paper.pdf)

[<img src="/images/Page1_Paper.png" alt="Page 1 Paper" width="30%">](#)

## Table of Contents 📑
- [Project Introduction](#project-introduction-)
- [Data Collection and Processing](#data-collection-and-processing-)
- [Methodology](#methodology-)
- [Results and Insights](#results-and-insights-)
- [Future Work](#future-work-)
- [Team](#team)
- [Contact](#contact-)
- [Code & Final Thoughts](#code-final-thoughts-)

## Project Introduction 📖
Our goal was to provide airlines with actionable recommendations for their in-flight entertainment offerings, predicting which media items are preferred by passengers and suggesting optimal changes to the media load. This includes both recommendations for media to remove (Recommendation I) and suggestions for new media to add (Recommendation II).

[<img src="/images/World_Map.png" alt="World Map with In-Flight Data" width="70%">](#)

## Data Collection and Processing 📊
We analyzed five months of historical flight data from Singapore Airlines, focusing on various aspects such as media usage and flight details. The data was thoroughly cleansed and prepared for analysis, involving steps like dimension reduction, data manipulation, and missing data imputation.

- **Flight Data Example**: Includes flight number, departure airport, seat number, departure date, and media ID.
- **Media Data Example**: Details media titles, types, release years, genres, and viewer scores.

[<img src="/images/Data_Extract.png" alt="Data Snapshot" width="70%">](#)

[<img src="/images/Aggregation.png" alt="Data Aggregation" width="70%">](#)

### Feature Engineering 
We enhanced our dataset by introducing features such as seat class, release year category, A-list actors, and price tags, significantly improving the predictive power of our models.

- **Key Features**:
    - A-List Actors: Number of top-grossing actors in a title.
    - Proportion Viewed and Used: Metrics calculated to gauge viewer engagement.

[<img src="/images/Feature_Engineering.png" alt="Feature Engineering" width="70%">](#)

## Methodology 🔍
Our approach combined **Generalized Linear Modeling (GLM)** with **k-fold Cross-Validation** to predict the proportion of views for each media item. We focused on:
- **Model Optimization**: Utilized GLM for prediction with a logit link function due to the binary nature of our response variable (proportion views).

[<img src="/images/glm.png" alt="Methodology" width="70%">](#)

[<img src="/images/Cross_Validation.png" alt="Cross Validation" width="70%">](#)

### Advanced Techniques
- **Data Augmentation**: Enhanced media data using external datasets to fill missing values.
- **Predictive Modeling**: Employed GLM from the statemodel library in Python to forecast media performance on future flights.

## Results and Insights 📈

### Overview of Findings
Our project utilized advanced data analytics techniques, including Generalized Linear Modeling (GLM) and k-fold Cross-Validation, to optimize in-flight entertainment offerings. By analyzing five months of in-flight data from Singapore Airlines, our team developed a model to predict media popularity and viewer engagement, aiming to enhance passenger satisfaction and reduce content-related costs.

### Key Insights
- **Viewer Preferences**: Our analysis revealed that a small proportion of media titles are viewed by a majority of passengers, supporting the application of the Pareto Principle (80/20 rule) in media selection.
- **Recommendation System Efficiency**: The media load recommendation system demonstrated an ability to significantly reduce the number of low-performing media titles aboard, thereby cutting down on unnecessary costs without compromising the quality of in-flight entertainment.
- **Optimization of Media Content**: Strategic recommendations for media removal and addition were developed, which, if implemented, are projected to improve passenger satisfaction by up to 20%.

[<img src="/images/Results_Overview.png" alt="Results Overview" width="70%">](#)

### Detailed Results
- **Proportion of Views Predicted**: Our model effectively predicted with a 75% accuracy the proportion of views for new media titles, facilitating proactive adjustments to the media catalog.
- **Media Popularity Factors**: Analysis identified key factors influencing media popularity, including media type, flight duration, and viewer demographics.
- **Cost Savings**: By implementing the recommended changes to the media load, airlines could potentially see a reduction in content-related expenditures by approximately 15% while maintaining or even improving passenger satisfaction.

[<img src="/images/Result1_Scenario1.png" alt="Prediction vs Baseline" width="70%">](#)

[<img src="/images/Result2-3_Scenario1.png" alt="In-Flight Media Selection" width="70%">](#)

### Impact on In-Flight Entertainment
Implementing our recommendations could lead to a more tailored in-flight entertainment experience, where passengers are more likely to find media that aligns with their preferences. Additionally, our predictive model allows airlines to stay ahead of trends by adjusting content based on anticipated viewer engagement.

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

## Code & Presentation 👨‍💻 

- Go through the Machine Learning Python code here: [Python Code](/Code/Python_for_ML/)
- Go through the Data Cleaning R code here: [R Code](/Code/R_for_cleaning/)
- Go through the presentation results here: [In-Flight Media Content Optimization Slides](/Final_slides.pptx)

## Contact 📬
For more information on this project, please reach out at [louisbenss@gmail.com](mailto:louisbenss@gmail.com).

Project Link: [https://github.com/LouisBensard/ML-Project01_In-Flight-Media-Optimization.git](https://github.com/LouisBensard/ML-Project01_In-Flight-Media-Optimization.git)

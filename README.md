### cs122_finalproject

# **Moving to Chicago and Don't Know Where to Live? Look No Further! Chicago Neighborhood and Property Finder**

## **Project Description**
Our project will allow users to input personal information such as age, gender, race, income, and the Chicago neighborhood that they live in and receive an estimate of their life expectancy based on these factors. Once given this initial output, users will be able to interact with sliding scales to adjust their input factors and see how their life expectancy may change as they alter their original input factors. 

## **Visualization** 
Users of the final product will be prompted to input a variety of information such as age, sex, income and locational data. The Matplot library and the Seaborn library will be used to display a plot with income as the independent variable and life-expectancy as the dependent variable. The fitted-model will take in additional parameters that the users has inputted and will be depicted on the plot. On the bottom of the plot a slider will allow the user to change their income level and see in real time how income changes could affect their estimated life-expectancy. The feasibility of adding sliders for non-continuous variables such as age and race will be explored with the possibility of changing the displayed independent variable on the graph. In addition, a map of Chicago centered on the user’s location will display the nearest health centers within a specified radius. This will likely be achieved with the Matplotlib, Cartopy, and Geopandas libraries.   

## **Approximate Methodology**
We can use linear regression to get our best estimates for this problem. Some of the variables we might consider are listed above in the “Project Description” section. We can start by comparing simple linear regression models then see how considering more variables impacts the accuracy and potential overfitting. Perhaps truer to real life, we would consider interaction effects between certain variables in an attempt to improve the overall model. 

## **Project Goal**
Through this project, we hope to provide an engaging platform for individuals to observe how many societal factors may affect one’s life expectancy. We hope to further elucidate factors that may provide greater contextualization for what recent research and reporting has termed the “life expectancy” gap across the city of Chicago.

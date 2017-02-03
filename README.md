#Predicting the Likes Count of a YouTube Video

The final project report can be accessed at - [Report](https://gitlab.com/mayank26saxena/PS17_Mayank_Saxena/blob/master/Mayank_Saxena_Report.pdf)

A command line tool to model the likes count of a YouTube video as a function of various
features. Since this task focused on feature engineering I have tried to obtain relevant features for the data set from different
methods and sources. I have used the YouTube API to gather video details such as -
- View Count
- Comment Count
- Dislike Count
- Favorite Count
- Life of video
- Duration
- Category etc.

Another set of features was gathered from the characteristics of the channel via which the video was uploaded. Some of the features in this category were -
- Channel Subscriber Count
- Channel View Count 
- Channel Video Count
- Channel Comment Count

The third method I used for feature engineering was finding out the number of times the video was shared on other social media platforms such as Facebook, Google Plus, Linkedin and Pinterest. Hence the next 5 features were generated as well -
- Facebook Shares
- Google Plus Shares
- LinkedIn Shares
- Pinterest Shares
- Total Shares

The model which I used was the Stochastic Gradient Descent based Linear Regression model. This module was imported from the [Scikit Learn](http://scikit-learn.org/) library. The best results (with highest R<sup>2</sup> error) were obtained with the following parameters :
- loss = squared_epsilon_insensitive
- penalty = none
- alpha = 1e-05

## How to Use
I have developed a command line tool to test out the model. 

1) <code>git clone https://github.com/mayank26saxena/PS17_Mayank_Saxena.git</code>

2) <code>cd PS17_Mayank_Saxena</code>

3) Run the <code>test_input.py</code> and provide the video ID as system arguement.

## Limitations
The file <code>get_data.py</code> can be run by providing the video ID as a command line arguement. The output will be the predicted like count , the actual like count and the error.

The high error in a few cases can be attributed to the fact that the data set is highly skewed with large number of videos having single digit or no likes but very few videos having likes greater than 10,000 with the highest like count of any video in the data set being <code>936889</code>

This error can be improved by collecting more data so that the data set is less skewed and more evenly distributed.

## Conclusion and Future Work
The first conclusion which can be drawn from this research is that the popularity of a video in terms of its like count can be predicted fairly well from features such as the view count, comment count, dislike count, channel subscriber count, channel video count, total shares across social media platforms along with features such as finding out whether the description of the video contains links to any third party website or any other social media platforms such as Facebook, Twitter, Instagram etc.

Future research should also look into deriving features from image thumbnails.  Intuition says that perhaps the presence of people’s faces in video thumbnails results in more likes than when it is not.

Another area where this model can be improved is by considering the content of the video into account. For example, if the person in the video asks the viewer to like the video then the viewers are more likely to like the video. Similarly, supposing a YouTuber announces a prize give away competition and asks the people to like the video to get enrolled in the competition, there will definitely be a higher number of likes on that video.


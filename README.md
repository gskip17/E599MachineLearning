# E599MachineLearning

For current dependency installation -
``` pip install --upgrade google-api-python-client ```

To run this project in it's current form simply run
``` python data_aggregator.py ```

The goal of this Machine Learning project is to model popularity of TedTalk lectures and accurately predict the popularity of a talk given based on categorical features such as the Title, Topic, Keywords, Date, and more. The data-set used for modeling currently come from the [Youtube Data API](https://developers.google.com/youtube/v3/libraries).

For this first commit, the program uses the Youtube Data API to grab data on from every single video uploaded by the ["TEDtalksDirector"](https://www.youtube.com/user/TEDtalksDirector/featured) channel on Youtube.

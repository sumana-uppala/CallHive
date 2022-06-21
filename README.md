# CallHive

Introduction to SER:
Emotion detection is a challenging task, because emotions are subjective. We define a SER system as a collection of methods that process and classify speech signals to detect emotions embedded in them. There are three classes of features in a speech namely, lexical features, visual features and acoustic features. We have built our project using the analysis of the acoustic features, that can be done in real-time while the conversation is taking place as we’d just need the audio data for accomplishing our task.

Salient features of SER:
1) Datasets that have been used:
The datasets are multimodal with gender balanced.
The data used in this project was combined from three different data sources as mentioned below:
TESS ,SAVEE, RAVDESS (Ryerson Audio-Visual Database of Emotional Speech and Song)
The datasets had many emotions like happy, fear, angry, calm, neutral, etc. and there were voices of both male and female.
2) Extracting features:
From audio data, we have extracted a key feature which have been used in this study, namely, MFCC((Mel Frequency Cepstral Coefficients) which is by far the most researched about and utilized features.
3) Machine learning model:
Using the extracted features, we have built a machine learning model using convolutional neural networks, trained the model with the dataset and saved it.
Here is the link to the model - https://github.com/sumana-uppala/CallHiveModel.git
4) SER website:
The ERSS calls are sent as input to the website. The ML model is pre-loaded in the website. So, the features are extracted from the audio and the ML model's predictiction is the output.


To run the code:

> git clone https://github.com/sumana-uppala/CallHive.git

> cd CallHive

> virtualenv venv

> source venv/bin/activate

> pip install -r requirements.txt

> python manage.py runserver

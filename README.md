# Scalable Machine Learning and Deep Learning - Lab1: Titanic Dataset Classifier

#  Github repository:
https://github.com/daniel-rdt/serverless_ml_titanic_dr

# File running sequence for titanic survival prediction:
1. run: python titanic-feature-pipeline.py
2. run: python titanic-training-pipeline.py
3. upload huggingface-spaces-titanic folder files to HuggingFace

Hugging Face Spaces public URL: https://huggingface.co/spaces/daniel-rdt/titanic

# File running sequence for titanic survival prediction for most recent passenger added:
4. run: python titanic-batch-inference-pipeline.py
5. run: python titanic-feature-pipeline-daily.py
6. upload huggingface-spaces-titanic-monitor folder files to HuggingFace

Hugging Face Spaces public URL: https://huggingface.co/spaces/daniel-rdt/titanic_monitor

# File explanation:
titanic_feature_prep.py:
- downloading data from github repository;
- feature engineering: 
- 1. removed "PassengerId","Name","Ticket" and "Cabin" columns;
- 2. age less than 1 year is rounded up to 1;
- 3. created random age values;
- 4. filled missing values for "Embarked" with "Unknown"; ------------------------------------------------
- 5. turned categorical variables ("Embarked" and "Sex") into numerical variables;
- 6. droped old categorical columns "Sex" and "Embarked"; ----------------------------

titanic-feature-pipeline.py:
- uploading data to Modal;
- storing features and labels into Hopsworks;

titanic-training-pipeline.py:
- uploading features and labels to Modal;
- running deep learning algorithm;
- storing model to Hopsworks;

huggingface-spaces-titanic folder:
- folder containing main app for user interface and requirements;

titanic-batch-inference-pipeline.py:
- uploading features to Modal;
- predicts if the synthetic passengers survived or not;
- storing predictions to Hopsworks;

titanic-feature-pipeline-daily.py:
- generating new random passenger every day;

huggingface-spaces-titanic-monitor folder:
- folder containing main app for user interface and requirements;
- shows the most recent synthetic passenger prediction and outcome, and a confusion matrix with historical prediction performance; 

# General notes
- everyone aged less than 1 year old is considerd as 1 year old person;
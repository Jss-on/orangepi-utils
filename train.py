import os
import numpy as np
from scipy.io import wavfile
from python_speech_features import mfcc
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import confusion_matrix, classification_report
import optuna
import joblib
import matplotlib.pyplot as plt
import seaborn as sns


# 1. Data Preprocessing
def load_audio_files_and_labels(root_folder):
    X, y = [], []
    for label in os.listdir(root_folder):
        label_folder = os.path.join(root_folder, label)
        if os.path.isdir(label_folder):
            for filename in os.listdir(label_folder):
                if filename.endswith(".wav"):
                    filepath = os.path.join(label_folder, filename)
                    sample_rate, audio_data = wavfile.read(filepath)
                    X.append(audio_data)
                    y.append(label)
    return X, y


# 2. Feature Extraction
def extract_mfcc_features(audio_data_list, sample_rate=16000):
    mfcc_features_list = []
    for audio_data in audio_data_list:
        mfcc_features = mfcc(audio_data, sample_rate)
        mfcc_features_list.append(np.mean(mfcc_features, axis=0))
    return np.array(mfcc_features_list)


# 3. Training Pipeline
pipeline = Pipeline([("clf", RandomForestClassifier())])


# 4. Hyperparameter Optimization
def objective(trial):
    n_estimators = trial.suggest_int("clf__n_estimators", 2, 50)
    max_depth = trial.suggest_int("clf__max_depth", 1, 10)
    min_samples_split = trial.suggest_int("clf__min_samples_split", 2, 10)
    criterion = trial.suggest_categorical(
        "clf__criterion", ["gini", "entropy"]
    )  # New line

    pipeline.set_params(
        clf__n_estimators=n_estimators,
        clf__max_depth=max_depth,
        clf__min_samples_split=min_samples_split,
        clf__criterion=criterion,  # New line
    )

    return np.mean(cross_val_score(pipeline, X_train, y_train, n_jobs=-1, cv=3))


# Function to display confusion matrix
def display_confusion_matrix(y_true, y_pred, labels):
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels
    )
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title("Confusion Matrix")
    plt.show()


if __name__ == "__main__":
    # Path to root folder containing audio data folders
    root_folder = "data"

    # 1. Load audio files and labels
    X, y = load_audio_files_and_labels(root_folder)

    # 2. Extract MFCC features
    X_mfcc = extract_mfcc_features(X)

    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X_mfcc, y, test_size=0.2, random_state=100
    )

    # Optimize hyperparameters
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=50)

    # Train and save the best model
    best_params = study.best_params
    print(best_params)
    pipeline.set_params(**best_params)
    pipeline.fit(X_train, y_train)
    joblib.dump(pipeline, "best_audio_classifier_v1.pkl")

    # Make predictions on the test set
    y_pred = pipeline.predict(X_test)

    # Display the confusion matrix
    unique_labels = np.unique(y)
    display_confusion_matrix(y_test, y_pred, labels=unique_labels)

    # Display the classification report
    print("Classification Report:")
    print(classification_report(y_test, y_pred, target_names=unique_labels))

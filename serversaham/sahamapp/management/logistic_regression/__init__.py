import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def proses_log_regresi(file, col_names = ['pregnant', 'glucose', 'bp', 'skin', 'insulin', 'bmi', 'pedigree', 'age', 'label'],
                       target = 'label'):

    # load data
    pima = pd.read_csv(file, header=0, names=col_names)
    print(pima.head())
    print('-'*10)

    #deteksi independent dan dependent variabel
    feature_cols = col_names

    X = pima[feature_cols] # Features
    y = pima['{}'.format(target)] # Target variable

    print(X, y)

    # split data: sebagian untuk training, sebagian untuk target (verifikasi)
    # dibagi menjadi dua: 75% training, 25% testing

    X_train, X_test, y_train, y_test=train_test_split(X, y, test_size=0.25, random_state=0)


    #bangun model regression
    logreg = LogisticRegression()

    #fit model dengan data
    print(y_train)
    logreg.fit(X_train, y_train)
    y_pred = logreg.predict(X_test)

    #evaluasi model: convusion matrix. Seberapa jauh kebenaran model kita?


    cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
    print(cnf_matrix) # 119 dan 36 prediksi benar, dan 26, 11  adalah prediksi salah

    #visualisasi
    class_names=[0,1] # name  of classes
    fig, ax = plt.subplots()
    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names)
    plt.yticks(tick_marks, class_names)

    # create heatmap
    sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu" ,fmt='g')
    ax.xaxis.set_label_position("top")
    plt.tight_layout()
    plt.title('Confusion matrix', y=1.1)
    plt.ylabel('Actual label')
    plt.xlabel('Predicted label')

    """
    Akurasi: tingkat akurasi
    Precision: Prediksi kebenaran kasus baru 76% 
    Recall: Deteksi data yang sudah ada, dengan kebenaran 58% 
    """
    print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
    print("Precision:",metrics.precision_score(y_test, y_pred))
    print("Recall:",metrics.recall_score(y_test, y_pred))
    plt.show()

    # tradeoff antara ketepatan dan akurasi
    """
    Kurva ROC 
    Kurva Receiver Operating Characteristic(ROC) menggambarkan nilai TP vs FP
    Nilai AUC 0.86, dimana AUC= 1 adalah model clasifier yang sempurna, dan 0.5 menandakan batas bawah classifier yang useless
    """
    y_pred_proba = logreg.predict_proba(X_test)[::, 1]
    fpr, tpr, _ = metrics.roc_curve(y_test, y_pred_proba)
    auc = metrics.roc_auc_score(y_test, y_pred_proba)
    plt.plot(fpr, tpr, label="data 1, auc=" + str(auc))
    plt.legend(loc=4)
    plt.show()

proses_log_regresi('test_data.csv',
                   col_names=['index','PassengerId','Survived','Sex','Age','Fare','Pclass_1','Pclass_2','Pclass_3','Family_size','Mr','Mrs','Master','Miss','Emb_1','Emb_2','Emb_3'],
                   target='Survived')
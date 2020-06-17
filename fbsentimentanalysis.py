import csv
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import xlrd
import openpyxl


#Reading CSV exported from facepager and converting it into .xlsx
read_file = pd.read_csv (r"C:\\FacebookCSV\\Facebook.csv" , delimiter=';')
write_file = read_file.to_excel (r"C:\\FacebookCSV\\FacebookEXCL.xlsx", index = None, header=True)

#Location of .xlsx file
loc = "C:\\FacebookCSV\\FacebookEXCL.xlsx"

def runAnalysis():
    sentences = []
    #Reading comments from facebookEXCL file
    wb = xlrd.open_workbook(loc, encoding_override="cp1252")
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 9)
    for i in range(sheet.nrows): 
        sentences.append(sheet.cell_value(i, 9))
    sid = SentimentIntensityAnalyzer()
    lol = []
    #Removing empty messages
    updated_sentences = [i for i in sentences if i]
    #Reading all the comments one by one and doing its sentiment analysis
    for sentence in updated_sentences:
        # print (sentence)
        ss = sid.polarity_scores(sentence)
        if ss['compound'] >= 0.05:
            sentiment = 'Positive'
        if ss['compound'] <= -0.05:
            sentiment = 'Negative'
        if ss['compound'] < 0.05 and ss['compound'] > -0.05:
            sentiment = 'Neutral'
        ss['sentence'] = sentence
        ss['sentiment'] = sentiment
        lol.append(ss)
    #Dataframe to create new csv file with expected results
    df = pd.DataFrame(lol)
    df = df[['sentence' , 'neg' , 'neu' , 'pos' , 'compound' , 'sentiment']]
    df.to_csv('C:\\Users\\mohd.arif.siddiqui\\Desktop\\Abhishek\\facebooksentiments.csv')
    print ("CSV file created with sentiment analysis")

def main():
    runAnalysis()

if __name__ == "__main__":
    main()


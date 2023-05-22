import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
df=pd.read_csv('articles.csv',encoding='utf-8'     )
analyze=SentimentIntensityAnalyzer()
negative=[]
neutral=[]
positive=[]
for n in range(df.shape[0]):
    title=df.iloc[n,0]
    description=df.iloc[n,2]
    title_analyzed=analyze.polarity_scores(title)
    description_analyzed=analyze.polarity_scores(description)
    negative.append(title_analyzed["neg"]+(description_analyzed["neg"])/2)
    neutral.append(title_analyzed["neu"]+(description_analyzed["neu"])/2)
    positive.append(title_analyzed["pos"]+(description_analyzed["pos"])/2)
df["Negative"]=negative
df["Neutral"]=neutral
df["Positive"]=positive
pd.set_option("display.max_columns",None)
# Save DataFrame to Excel
output_filename = "sentiment_analysis.xlsx"
df.to_excel(output_filename, index=False)
import pandas as pd

df = pd.read_csv('Training.csv')


li = df.prognosis.unique()
for l in li:
	if(l == "Peptic ulcer diseae" ):
		continue
	print(l)
	if(l == "Fungal infection"):
		Disease.objects.get(Name=l.strip())
		exit(0)
	
from turtle import width
import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

image = Image.open('dna-logo.jpg')

st.image(image, use_column_width=True)

st.write ("""
# DNA Nucleotide Count Web App

This App counts the nucleotide composition of query DNA!

***
""")

st.header('Enter DNA sequence')
sequence_input =">DNA Query 2\nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"

sequence = st.text_area("Sequence input", sequence_input, height=250)
sequence = sequence.splitlines()
# sequence
sequence = sequence[1:]
# sequence
sequence = ''.join(sequence)
# sequence

st.write("""
***
""")

st.header('OUTPUT (DNA Nucleptide Count)')

st.subheader('1. Print dictionary')
def DNA_nucleotide_count(seq):
    d=dict ([
        ('A',seq.count('A')),
        ('T',seq.count('T')),
        ('G',seq.count('G')),
        ('C',seq.count('C')),
    ])    
    return d

X= DNA_nucleotide_count(sequence)

X_label=list(X)
X_values=list(X.values())
X

st.subheader('2. Print text')
st.write('There are '+str(X['A'])+' adenine (A)')
st.write('There are '+str(X['T'])+' thymine (T)')
st.write('There are '+str(X['G'])+' guanine (G)')
st.write('There are '+str(X['C'])+' cytosnine (C)')

st.subheader('3. Display Dataframe')
df= pd.DataFrame.from_dict(X, orient='index')
df= df.rename({0:'count'}, axis='columns')
df.reset_index(inplace=True)
df=df.rename(columns={'index':'nucleotide'})
st.write(df)

st.subheader('4. Display bar Chart')
p = alt.Chart(df).mark_bar().encode(
    x='nucleotide',
    y='count'
)

p=p.properties(
    width=alt.Step(100)
)

st.write(p)
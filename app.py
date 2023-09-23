from flask import Flask, render_template,request
import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import ast

os.environ["OPENAI_API_KEY"] = "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"


app = Flask(__name__)

llm = OpenAI(temperature=0.2)

template_string_1 ="""You are a pharmacist specilized in medicine and you carry 50 years of experience. \
You have the knowledge of every medicine in the market. \
Kindly help me with the {medicine_1} and with your knowledge answer my query 
Description: Describe the medicine, its uses, and properties. ,\
Price: Mention the price range of the medicine in Indian rupees. ,\
Side_Effects: List potential side effects and adverse reactions.,\
Rate_and_Review: Provide a brief rating and review of the medicine between 1 to 5.\
and Generic_Alternatives: Name at least three generic alternatives for this medicine."
Format the output as JSON with the following keys:
"Name"
"Description"
"Price"
"Side_Effects"
"rate_and_review"
"Generic_Alternatives"
"""

template_string_2 ="""You are a pharmacist specilized in medicine and you carry 50 years of experience.\
You have the knowledge of every medicine in the market\
Kindly help me with the {medicine_2} and with your knowledge answer my query 
Description: Describe the medicine, its uses, and properties. ,\
Price: Mention the price range of the medicine in Indian rupees. ,\
Side_Effects: List potential side effects and adverse reactions.,\
Rate_and_Review: Provide a brief rating and review of the medicine between 1 to 5.\
and Generic_Alternatives: Name at least three generic alternatives for this medicine."
Format the output as JSON with the following keys:
"Name"
"Description"
"Price"
"Side_Effects"
"Rate_and_review"
"Generic_Alternatives"
"""


first_medicine = PromptTemplate(
    input_variables=['medicine_1'],
    template=template_string_1
    )
chain = LLMChain(llm=llm,prompt=first_medicine,verbose=True)

Second_medicine = PromptTemplate(
    input_variables=['medicine_2'],
    template=template_string_2
    )

chain2 = LLMChain(llm=llm,prompt=Second_medicine,verbose=True)


@app.route('/', methods=['GET', 'POST'])
def display_medicine_info():
    if request.method == 'POST':
        medicine_1 = request.form['medicine_1']
        medicine_2 = request.form['medicine_2']

        med_1 = chain.run(medicine_1)
        med_2 = chain2.run(medicine_2)
      
        output_1  = ast.literal_eval(med_1)
     
        output_2  = ast.literal_eval(med_2)


        return render_template('index.html', output1=output_1, output2=output_2)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

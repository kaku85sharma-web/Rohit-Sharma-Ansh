def llm_app(topic):
 import os
 from dotenv import load_dotenv
 from langchain_core.prompts import PromptTemplate
 from langchain_groq import ChatGroq
 # 1. Initialize your LLM
 load_dotenv()
groq_api_key = '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'

 llm = ChatGroq(model='openai/gpt-oss-120b', api_key=groq_api, temperature=0.1)

 prompt=PromptTemplate(
    input_variables=['topic'],
    
    template='You are a sign language expert.\
    provide five important lines coverng about {topic}.'
 )

 chain=prompt | llm

 #topic=input('Enter a topic')
 
 output=chain.invoke(topic)
 #print('Generated Blog Title ', output.content)
 return output.content

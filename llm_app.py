def llm_app(topic):
   
    from langchain_core.prompts import PromptTemplate
    from langchain_groq import ChatGroq

    


    # Groq API Key
    groq_api_key = "gsk_your_new_api_key"

    # Initialize LLM
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        api_key=groq_api_key,
        temperature=0.1
    )

    # Prompt Template
    prompt = PromptTemplate(
        input_variables=["topic"],
        template="""
You are a sign language expert.
Provide five important lines covering about {topic}.
"""
    )

    # Create chain
    chain = prompt | llm

    # Invoke the model
    output = chain.invoke({"topic": topic})

    return output.content

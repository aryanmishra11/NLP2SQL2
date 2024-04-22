# DESIGNING THE FRONT END 
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import os
#importing google's generative ai
import google.generativeai as genai

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
#configuring our API Key
genai.configure(api_key=GOOGLE_API_KEY)

#loaded Gemini pro model
model=genai.GenerativeModel('gemini-pro')

#main function under which all the implementation will go
def main():
    
    #setting up a page configuration with title
    st.set_page_config(page_title="SQL Query Generator",page_icon=":robot:")
    
    #creating a markdown which would give a plain HTML abiity
    st.markdown(
        """ 
            <div style="text-align: center;">
                <h1>SQL Query Generator</h1>
                <h3>I can generate SQL queries for you!</h3>
                <h4>With Explanation as well </h4>
                <p>This tool is a simple tool that allows you to generate SQL queries based on your prompts.</p>
            </div>
            
        """,
        unsafe_allow_html=True
    )
    
    text_input=st.text_area("Enter your Query here in plain English:")
    
    #generating response
    submit=st.button("Generate SQL Query")
    if submit:
        
        #spinning for loading
        with st.spinner("Generating SQL Query..."):
            
            template="""
                Create a SQL snippet using the below text:
                    ```
                    {text_input}    
                    ```
                    """
            formatted_template=template.format(text_input=text_input)
            st.write(formatted_template)
            response=model.generate_content(formatted_template)
            sql_query=response.text
            sql_query=sql_query.strip().lstrip("```sql").rstrip("```")
            # st.write(sql_query)
            
            expected_output="""
                What would be the expected response of this SQL Query snippet:
                
                    ```
                    {sql_query}
                    ```
                Provide sample tabular Response with no explanation:
                
            """
            expected_output_formatted=expected_output.format(sql_query=sql_query)
            eoutput=model.generate_content(expected_output_formatted)
            eoutput=eoutput.text
            #st.write(eoutput)
            
            explanation="""
                Explain this SQL Query:
                
                    ```
                    {sql_query}
                    ```
                Please provide with simplest of explanation:
                
            """
            explanation_formatted=explanation.format(sql_query=sql_query)
            explanation=model.generate_content(explanation_formatted)
            explanation=explanation.text
            #st.write(explanation)
            
            
            with st.container():
                st.success("SQL Query Generated Successfully! Here is your Query Below: ")
                st.code(sql_query,language="sql")
                
                st.success("Expected output of this SQL Query will be: ")
                st.markdown(eoutput)
                
                st.success("Explanation of this SQL Query: ")
                
                st.markdown(explanation)

main()
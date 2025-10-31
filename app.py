import streamlit as st
import pandas as pd
import groq
import time
import io
from contextlib import redirect_stdout

# --- 1. Set up the AI Client (Unchanged) ---
try:
    client = groq.Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"Error setting up Groq client: {e}. Make sure your GROQ_API_KEY is in secrets.toml.")
    st.stop()


# --- 2. Define Your Data File Paths ---
CROP_YIELD_PATH = "data/crop_yield_2019.csv"
CLIMATE_DATA_PATH = "data/Rainfall.xls"
OIL_SEED_PATH = "data/oil_seed.csv"  # <-- NEW 3RD DATASET


# ----------------------------------------------------
# STEP 3: CREATE YOUR "TOOLS" (THE "HANDS")
# ----------------------------------------------------

def query_crop_yield(question):
    """
    This is our "Smart Tool" for the main CROP YIELD data.
    """
    try:
        df = pd.read_csv(CROP_YIELD_PATH)
        df.columns = df.columns.str.strip().str.replace(' ', '_')
        column_names = df.columns.to_list()

        code_prompt = f"""
        You are an expert Python data analyst. You are given a pandas DataFrame 'df'
        with general CROP YIELD data.
        The user's question is: '{question}'
        The DataFrame's columns are: {column_names}

        Write a short Python script using the 'df' DataFrame to answer the question.
        Your script MUST end with a single print() statement that outputs the final answer.
        Do not write any explanation, just the Python code.

        Question: {question}
        Python Code:
        """
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": code_prompt}]
        )
        generated_code = response.choices[0].message.content.strip()
        
        if "```python" in generated_code:
            generated_code = generated_code.split("```python")[1].split("```")[0].strip()
        elif "```" in generated_code:
            generated_code = generated_code.split("```")[0].strip()

        f = io.StringIO()
        with redirect_stdout(f):
            exec(generated_code, {"df": df, "pd": pd})
        raw_data_output = f.getvalue().strip()
        
        if not raw_data_output:
            return {"answer": "Error: The AI ran code but it produced no output."}

        # --- Part 2: Clean Up the Raw Output ---
        cleanup_prompt = f"User Question: \"{question}\"\nRaw Data Answer: \"{raw_data_output}\"\nFriendly Answer:"
        cleanup_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": cleanup_prompt}]
        )
        friendly_answer = cleanup_response.choices[0].message.content.strip()

        return {
            "answer": friendly_answer,
            "source": CROP_YIELD_PATH
        }
    except Exception as e:
        return {"answer": f"Error: An error occurred: {e}\nGenerated code was:\n{generated_code}"}


def query_climate_data(question):
    """
    This is our "Smart Tool" for the CLIMATE data.
    """
    try:
        df = pd.read_excel(CLIMATE_DATA_PATH)
        df.columns = df.columns.str.strip().str.replace(' ', '_')
        column_names = df.columns.to_list()

        code_prompt = f"""
        You are an expert Python data analyst. You are given a pandas DataFrame 'df'
        with DISTRICT-WISE RAINFALL data.
        The user's question is: '{question}'
        The DataFrame's columns are: {column_names}

        Write a short Python script using the 'df' DataFrame to answer the question.
        Your script MUST end with a single print() statement that outputs the final answer.
        The 'ANNUAL' column contains the annual rainfall in millimeters.

        Question: {question}
        Python Code:
        """
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": code_prompt}]
        )
        generated_code = response.choices[0].message.content.strip()
        
        if "```python" in generated_code:
            generated_code = generated_code.split("```python")[1].split("```")[0].strip()
        elif "```" in generated_code:
            generated_code = generated_code.split("```")[0].strip()

        f = io.StringIO()
        with redirect_stdout(f):
            exec(generated_code, {"df": df, "pd": pd})
        raw_data_output = f.getvalue().strip()
        
        if not raw_data_output:
            return {"answer": "Error: The AI ran code but it produced no output."}

        # --- Part 2: Clean Up the Raw Output ---
        cleanup_prompt = f"User Question: \"{question}\"\nRaw Data Answer: \"{raw_data_output}\"\nFriendly Answer:"
        cleanup_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": cleanup_prompt}]
        )
        friendly_answer = cleanup_response.choices[0].message.content.strip()

        return {
            "answer": friendly_answer,
            "source": CLIMATE_DATA_PATH
        }
    except Exception as e:
        return {"answer": f"Error: An error occurred: {e}\nGenerated code was:\n{generated_code}"}


# --- THIS IS THE NEW OIL SEED TOOL ---
def query_oil_seed(question):
    """
    This is our "Smart Tool" for the OIL SEED data.
    """
    try:
        # --- Part 1: Generate and Run Code ---
        df = pd.read_csv(OIL_SEED_PATH) # <-- Reads CSV
        df.columns = df.columns.str.strip().str.replace(' ', '_')
        column_names = df.columns.to_list()

        code_prompt = f"""
        You are an expert Python data analyst. You are given a pandas DataFrame 'df'
        with specific OIL SEED production data.
        The user's question is: '{question}'
        The DataFrame's columns are: {column_names}

        Write a short Python script using the 'df' DataFrame to answer the question.
        Your script MUST end with a single print() statement that outputs the final answer.
        Do not write any explanation, just the Python code.

        Question: {question}
        Python Code:
        """
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": code_prompt}]
        )
        generated_code = response.choices[0].message.content.strip()
        
        if "```python" in generated_code:
            generated_code = generated_code.split("```python")[1].split("```")[0].strip()
        elif "```" in generated_code:
            generated_code = generated_code.split("```")[0].strip()

        f = io.StringIO()
        with redirect_stdout(f):
            exec(generated_code, {"df": df, "pd": pd})
        raw_data_output = f.getvalue().strip()
        
        if not raw_data_output:
            return {"answer": "Error: The AI ran code but it produced no output."}

        # --- Part 2: Clean Up the Raw Output ---
        cleanup_prompt = f"User Question: \"{question}\"\nRaw Data Answer: \"{raw_data_output}\"\nFriendly Answer:"
        cleanup_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": cleanup_prompt}]
        )
        friendly_answer = cleanup_response.choices[0].message.content.strip()

        return {
            "answer": friendly_answer,
            "source": OIL_SEED_PATH
        }
    except Exception as e:
        return {"answer": f"Error: An error occurred: {e}\nGenerated code was:\n{generated_code}"}


# ----------------------------------------------------
# STEP 4: CREATE YOUR "ORCHESTRATOR" (THE "BRAIN")
#   *** THIS IS THE UPGRADED 5-WAY ROUTER ***
# ----------------------------------------------------

def run_agent(user_question):
    """
    This agent classifies the question and then *routes*
    it to the correct tool(s).
    """
    
    # 1. Classify the question
    prompt = f"""
    You are an intelligent router. The user's question is: "{user_question}"
    
    Classify this question into one of five categories:
    1. 'GREETING' (for simple hellos, "how are you", "hi", etc.)
    2. 'CROP_YIELD' (for general questions about crops, yield, rice, wheat, etc.)
    3. 'CLIMATE_DATA' (for any question about rainfall, climate, weather, annual rainfall, etc.)
    4. 'OIL_SEED' (for specific questions about oil seeds, groundnut, mustard, soyabean, etc.)
    5. 'OTHER_QUESTION' (for anything else)
    
    Respond with *only* one word: GREETING, CROP_YIELD, CLIMATE_DATA, OIL_SEED, or OTHER_QUESTION.
    
    Example 1: "hi" -> GREETING
    Example 2: "what is the yield of wheat?" -> CROP_YIELD
    Example 3: "what is the rainfall in Pune?" -> CLIMATE_DATA
    Example 4: "what is the production of groundnut?" -> OIL_SEED
    Example 5: "what is your name?" -> OTHER_QUESTION
    """
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    classification = response.choices[0].message.content.strip().upper()

    # 2. Execute the correct path
    
    if "CROP_YIELD" in classification:
        data_result = query_crop_yield(user_question)
    
    elif "CLIMATE_DATA" in classification:
        data_result = query_climate_data(user_question)

    elif "OIL_SEED" in classification:
        data_result = query_oil_seed(user_question)

    elif "GREETING" in classification:
        greeting_answer = "Hello! I am the Project Samarth Q&A system. I can help you with questions about Indian crop yields, oil seeds, and climate data. What would you like to know?"
        return {"type": "greeting", "content": greeting_answer}
    
    else: # This covers 'OTHER_QUESTION'
        other_answer = "That's an interesting question! However, I can only answer questions about crop yields, oil seeds, and rainfall data. Try asking me a question about one of those topics."
        return {"type": "other", "content": other_answer}

    # 3. Format and return the data answer
    if "Error:" in data_result.get("answer", ""):
        return {"type": "error", "content": data_result["answer"]}
    
    formatted_answer = f"{data_result['answer']}\n\n*Source: {data_result['source']}*"
    return {"type": "data", "content": formatted_answer}


# ----------------------------------------------------
# STEP 5: BUILD THE FRONT-END (Unchanged)
# ----------------------------------------------------

st.title("Project Samarth 🇮🇳")
st.header("My Intelligent Q&A System")

user_question = st.text_input("Ask a question about agriculture or climate:")

# ----------------------------------------------------
# STEP 6: CONNECT THE FRONT-END TO THE "BRAIN"
# (Unchanged)
# ----------------------------------------------------

if user_question:
    st.divider()
    with st.spinner("Agent is working... Please wait."):
        agent_response = run_agent(user_question)
        response_type = agent_response["type"]
        response_content = agent_response["content"]
        
        if response_type == "error":
            st.error(response_content)
        elif response_type == "data":
            st.success("Here is your answer:")
            st.markdown(response_content)
        else: # "greeting" and "other"
            st.info(response_content)
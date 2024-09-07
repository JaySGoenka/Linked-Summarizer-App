import json
from langchain_ollama import OllamaLLM
from langchain.prompts.prompt import PromptTemplate

# Initialize the LLM (Ollama model)
model = OllamaLLM(model="llama3.1")

# Generate a summary from LinkedIn profile data using Llama3 model
def generate_summary(profile_data):
    template = """
        You are tasked with summarizing a person's professional background based on their LinkedIn profile data.
        Please provide a detailed and human-readable summary of the individual's skills, experiences, and expertise.
        
        Focus on:
        - Professional experiences and job roles.
        - Specific skills and technical expertise.
        - Notable achievements or accomplishments.
        - Certifications and education.
    
        DO NOT EXPALIN THE JSON. Instead extract information from the JSON and provide a summary.
        Provide the summary as if you are writing a description for a recruiter to understand the person's qualifications for a job role.
        Give a detailed summary with a professional tone, clear language and as descriptive as possible.
        Write the summary in a paragraph format.
        Here is the LinkedIn profile data:
        {profile_data}
    """

    profile_data_str = json.dumps(profile_data, indent=2)
    prompt = PromptTemplate(template=template, input_variables=["profile_data"])

    formatted_prompt = prompt.format(profile_data=profile_data_str) # Ensure formatted_prompt is a string
    print(f"Formatted Prompt Type: {type(formatted_prompt)}")

    print(f"Formatted Prompt: {formatted_prompt}")

    # Invoke the model with the formatted string
    try:
        response = model.invoke(formatted_prompt)  # Passing the prompt string directly
        return response if response else "Summary generation failed."
    except Exception as e:
        print(f"Error invoking model: {e}")
        return "Summary generation failed due to an error."

if __name__ == "__main__":
    profile_data = input("Enter the LinkedIn profile data: ")

    summary = generate_summary(profile_data)

    if summary:
        print("\nProfile Summary:")
        print(summary)
    else:
        print("Failed to generate profile summary.")

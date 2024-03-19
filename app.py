import os
import streamlit as st
from openai import AzureOpenAI

os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = "2023-05-15"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://pvg-azure-openai-uk-south.openai.azure.com"

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=st.secrets["AZURE_OPENAI_KEY"],
    api_version="2023-05-15"
)


def chat(prompt):
    response = client.chat.completions.create(
        model="gpt-35-turbo",  # model = "deployment_name".
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    answer = response.choices[0].message.content
    print(f"Answer is:{answer}")
    return answer


if __name__ == "__main__":

    st.title('Eva Chat')

    prompt = st.chat_input("Enter your questions here")

    if "user_prompt_history" not in st.session_state:
        st.session_state["user_prompt_history"] = []
    if "chat_answers_history" not in st.session_state:
        st.session_state["chat_answers_history"] = []
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    if prompt:
        with st.spinner("Generating......"):
            output = chat(prompt)
            st.session_state["chat_answers_history"].append(output)
            st.session_state["user_prompt_history"].append(prompt)
            st.session_state["chat_history"].append((prompt, output))

    # Displaying the chat history

    if st.session_state["chat_answers_history"]:
        for i, j in zip(st.session_state["chat_answers_history"], st.session_state["user_prompt_history"]):
            message1 = st.chat_message("user")
            message1.write(j)
            message2 = st.chat_message("assistant")
            message2.write(i)

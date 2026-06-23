from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

load_dotenv()

reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a strict editor and a viral influencer grading an email or a post. "
            "Provide a detailed, concrete critique. Identify missing information, logial flaws, "
            "or stylistic problems. Generate recommendations for the user. "
            "If the text is absolutely perfect, explicitly reply with only one word 'APPROVED'. "
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert writer. Write a comprehensive, clear articles to the topic requested. "
            "If critique or recommendation is provided in the chat history, "
            "strictly update your response to fix all highlighted issues. "
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

llm = ChatOpenAI(model="gpt-5.4-mini", temperature=0.5)
generate_chain = generation_prompt | llm
reflect_chain = reflection_prompt | llm

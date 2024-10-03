# Playground used to experiment with Streaming

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

chat = ChatOpenAI()

prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{content}"),
    ]
)

chain = LLMChain(llm=chat, prompt=prompt)

output = chain("Tell me a joke.")
print(output)

messages = prompt.format_messages(content="tell me a joke")

# Create generator output
output = chat.stream(messages)

for message in output:
    print(message.content)

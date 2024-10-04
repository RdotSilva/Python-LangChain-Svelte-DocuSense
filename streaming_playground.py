# Playground used to experiment with Streaming

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackHandler
from dotenv import load_dotenv

load_dotenv()


class StreamingHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token, **kwargs):
        print(token)


chat = ChatOpenAI(streaming=True)

prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{content}"),
    ]
)

chain = LLMChain(llm=chat, prompt=prompt)

output = chain.stream(input={"content": "Tell me a joke."})

for item in output:
    print(item)

# messages = prompt.format_messages(content="tell me a joke")

# # Create generator output
# output = chat.stream(messages)

# for message in output:
#     print(message.content)

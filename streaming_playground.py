# Playground used to experiment with Streaming

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackHandler
from dotenv import load_dotenv
from queue import Queue

load_dotenv()

queue = Queue()


class StreamingHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token, **kwargs):
        queue.put(token)


chat = ChatOpenAI(
    streaming=True,
    callbacks=[StreamingHandler()],
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{content}"),
    ]
)


class StreamingChain(LLMChain):
    def stream(self, input):
        print(self(input))  # Reference to the chain
        yield "hi"
        yield "there"


chain = StreamingChain(llm=chat, prompt=prompt)

for output in chain.stream(input={"content": "Tell me a joke"}):
    print(output)

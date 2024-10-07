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
        """
        Check for each token in the queue and return the each token in a stream

        :param input: The input of the chain

        :return: A token

        Example Usage:

        chain = chain.stream(input={"content": "Tell me a joke"}):
        """
        self(input)
        while True:
            token = queue.get()
            yield token


chain = StreamingChain(llm=chat, prompt=prompt)

for output in chain.stream(input={"content": "Tell me a joke"}):
    print(output)

# Playground used to experiment with Streaming

from typing import Any
from uuid import UUID
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackHandler
from dotenv import load_dotenv
from queue import Queue
from threading import Thread

load_dotenv()


class StreamingHandler(BaseCallbackHandler):
    def __init__(self, queue):
        self.queue = queue

    def on_llm_new_token(self, token, **kwargs):
        self.queue.put(token)

    def on_llm_end(self, response, **kwargs):
        self.queue.put(None)

    def on_llm_error(self, error, **kwargs):
        self.queue.put(None)


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

        queue = Queue()
        handler = StreamingHandler(queue)

        def task():
            self(input)

        Thread(target=task).start()

        while True:
            token = queue.get()
            if token is None:
                break
            yield token


chain = StreamingChain(llm=chat, prompt=prompt)

for output in chain.stream(input={"content": "Tell me a joke"}):
    print(output)

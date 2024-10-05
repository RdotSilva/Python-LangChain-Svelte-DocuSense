# Playground used to experiment with Streaming

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackHandler
from dotenv import load_dotenv

load_dotenv()


class StreamingHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token, **kwargs):
        # TODO: update logic
        pass


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
        print("Hello World")


chain = StreamingChain(llm=chat, prompt=prompt)

chain.stream("FAKETEXT")

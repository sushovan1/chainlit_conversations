# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 12:28:25 2024

@author: CSU5KOR
"""

import chainlit as cl
import openai
openai.__version__

from openai import OpenAI
from openai import AsyncOpenAI

client = AsyncOpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)
settings = {
    "model": "google/gemma-7b-it:free",
    "temperature": 0.7,
    "max_tokens": 500,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}
##########################################################################
@cl.on_chat_start
def start_chat():
    cl.user_session.set(
       "message_history",
       [{"role": "system", "content": "You are a helpful assistant."}],
   )

@cl.on_message
async def main(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")
    await msg.send()

    stream = await client.chat.completions.create(
        messages=message_history, stream=True, **settings
    )

    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await msg.stream_token(token)

    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()
#####################################################################
"""@cl.on_message
async def main(message: cl.Message):
   contents = message.content
   completion = client.chat.completions.create(
     model="google/gemma-7b-it:free",
     messages=[
       {
         "role": "user",
         "content": contents,
       },
     ],
   )
   message_to_send=completion.choices[0].message.content

   await cl.Message(message_to_send).send()"""
#############################################################################


"""@cl.on_chat_start

def on_chat_start():
    print("A new session")

@cl.on_message
async def on_message(msg: cl.Message):
    response=f"user has given the input: {msg.content}"
    await cl.Message(response).send()"""


"""@cl.on_message
async def on_message(message: cl.Message):
    response = f"Hello, you just sent: {message.content}!"
    await cl.Message(response).send()"""
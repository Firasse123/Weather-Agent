import asyncio
from urllib import response
from sqlalchemy import text
from typing_extensions import final
from llama_index.core.agent.workflow import ReActAgent
from llama_index.core.workflow import Context
from llama_index.llms.ollama import Ollama 
from llama_index.core.agent.workflow import AgentStream
from tool import weather_tool
def get_agent():
    # Context for the agent
    context = "You are a helpful assistant that provides weather information using the OpenWeatherMap API."
    
    # Initialize Ollama LLM
    llm = Ollama(
        model="llama3.1:latest",
        request_timeout=120.0
    )
    
    # Create ReAct agent
    agent = ReActAgent(
        llm=llm,
        tools=[weather_tool],
        verbose=True,
        context=context
    )
    
    # Create context
    ctx = Context(agent)
    
    # Start chat loop
    return agent,ctx


async def weather(agent, message, ctx):
        try:
            handler = agent.run(message, ctx=ctx)
            
            # Stream the response
            print("Assistant: ", end="", flush=True)
            async for ev in handler.stream_events():
                if isinstance(ev, AgentStream):
                    print(ev.delta, end="", flush=True)
            
            # Get final response
            final = await handler
            final_text = str(final)
            # prefer the streamed text if present, else final_text
            return final_text
            
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.\n")




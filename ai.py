# import anthropic
from groq import Groq
from dotenv import load_dotenv
import os
from pathlib import Path
import json
from tools import search, browse, type_content
from memory import delete_conversation, create_conversation, list_conversations

env_path = Path.home() / "jarvis" / ".env"
load_dotenv(dotenv_path=env_path)
# anthropic_key = os.getenv("ANTHROPIC_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")


# def get_ai_response_anthropic(text):
#     client = anthropic.Anthropic(api_key=anthropic_key)
#     message = client.messages.create(
#         model ="claude-opus-4-5",
#         max_tokens=1024,
#         messages=[
#             {"role": "user", "content": text}
#         ]
#     )
    
#     return message.content[0].text

# print(get_ai_response("print('hello world')"))

jarvis_tools = [
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "Search a phrase on duckduckgo",
            "parameters": {
                "type": "object",
                "properties": {
                    "search_phrase": {
                        "type": "string",
                        "description": "The search phrase to put into the engine"
                    },
                    "results_amount": {
                        "type": "integer",
                        "description": "Maximum number of search results to return, default is 5"
                    }
                },
                "required": ["search_phrase"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "browse",
            "description": "Fetches html from a url and returns it in plain text",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The url for the html to fetch"
                    }
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_conversations",
            "description": "List all available conversations",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_conversation",
            "description": "Create a new conversation",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the conversation"
                    }
                },
                "required": ["name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_conversation",
            "description": "Delete a conversation",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the conversation to delete"
                    }
                },
                "required": ["name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "type_content",
            "description": "type out any information you think I might want to know and that is inefficient to say through tts, eg. urls",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "all of the information you want to tell me, format it nicely"
                    },
                },
                "required": ["content"]
            }
        }
    }
]
avaliable_functions = {
    "search": search,
    "browse": browse,
    "create_conversation": create_conversation,
    "list_conversations": list_conversations,
    "delete_conversation": delete_conversation,
    "type_content" : type_content
}

def get_ai_response_groq(text, conversation):
    client = Groq(
    api_key=groq_key,
    )
    conversation.append({"role": "user", "content": text})
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are Jarvis, an advanced AI voice"
            "assistant running on an Arch Linux machine." 
            "Your most important trait is giving clear, concise,"
            "no-fluff answers. Be direct. You communicate via voice"
            "— responses must be short, natural when spoken, and contain"
            "no markdown, bullet points, or lists. Address me as 'sir'."
            "Your tone is formal but dry and subtly sarcastic. Never use"
            "filler phrases like 'certainly', 'great question', 'of course'"
            ", or 'absolutely'. When you have used the type_content tool,"
            "your spoken response should only acknowledge that you've typed the information"
            "nothing else. Never include raw function calls, JSON,"
            "or HTML in your spoken response."

        }
    ] + conversation,
    model="llama-3.3-70b-versatile",
    tools=jarvis_tools
    )

    while chat_completion.choices[0].finish_reason == "tool_calls":
        tool_choice = chat_completion.choices[0].message.tool_calls[0]
        function = tool_choice.function.name
        args = json.loads(tool_choice.function.arguments)
        tool_result = avaliable_functions[function](**args)
    
        
        chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content":
            "You are Jarvis, an advanced AI voice"
            "assistant running on an Arch Linux machine." 
            "Your most important trait is giving clear, concise,"
            "no-fluff answers. Be direct. You communicate via voice"
            "— responses must be short, natural when spoken, and contain"
            "no markdown, bullet points, or lists. Address me as 'sir'."
            "Your tone is formal but dry and subtly sarcastic. Never use"
            "filler phrases like 'certainly', 'great question', 'of course'"
            ", or 'absolutely'. When you have used the type_content tool,"
            "your spoken response should only acknowledge that you've typed the information"
            "nothing else. Never include raw function calls, JSON,"
            "or HTML in your spoken response."}] + conversation + [
            chat_completion.choices[0].message,  
            {
                "role": "tool",
                "tool_call_id": tool_choice.id,
                "content": json.dumps(tool_result)
            }
        ],
        model="llama-3.3-70b-versatile",
        tools=jarvis_tools,
        parallel_tool_calls=False
        )

    conversation.append({"role": "assistant", "content": chat_completion.choices[0].message.content})
    print(type(chat_completion.choices[0].message.content))
    print(type(conversation))
    return chat_completion.choices[0].message.content, conversation




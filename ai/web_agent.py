import os
from dotenv import load_dotenv
from tavily import TavilyClient
from openai import OpenAI

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def search_web(query):

    results = tavily.search(
        query=query,
        search_depth="advanced",
        max_results=8
    )

    contents = []
    sources = []

    for r in results["results"]:
        contents.append(r["content"])
        sources.append(r["url"])

    return contents, sources


def ask_web_agent(question, chat_history):

    contents, sources = search_web(question)

    context = "\n\n".join(contents)

    messages = [
        {
            "role": "system",
            "content": """
You are a helpful AI tech assistant.

Answer the question using the provided web search context.

Provide a clear structured answer.

Use sections like:
Programming
Tools
Concepts
Frameworks

Keep the answer concise and informative.
"""
        }
    ]

    messages += chat_history

    messages.append({
        "role": "user",
        "content": f"""
Context from web search:
{context}

Question:
{question}
"""
    })

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    answer = response.choices[0].message.content

    return answer, sources
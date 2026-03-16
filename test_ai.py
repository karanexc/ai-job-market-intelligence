from ai.sql_agent import ask

question = "What are the most demanded skills?"

result = ask(question)

print("\nQuery Result:\n")
for r in result:
    print(r)
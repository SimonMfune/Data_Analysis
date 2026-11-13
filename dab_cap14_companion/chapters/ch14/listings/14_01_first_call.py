client = get_client()                      # LLM_PROVIDER in .env decides; the default is "mock"
reply = client.complete("In one sentence, what is gross margin?",
                        system="You are a concise assistant for retail analysts.")
print(f"Provider: {reply.provider}   model: {reply.model}")
print(f"Tokens in/out: {reply.input_tokens}/{reply.output_tokens}   seconds: {reply.seconds}")
print(reply.text)

reply = client.complete(prompt, system=system)
print(reply.text)
print(f"\n[{reply.provider}, {reply.input_tokens} tokens in, {reply.output_tokens} out]")

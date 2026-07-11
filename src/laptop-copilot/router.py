#What it does: Decides where user requests should go.
#Logic used: Routing/orchestration logic; it inspects intent and decides whether to call tools,
#memory, model services, or UI actions.
#Interconnection: Likely sits between ui/cli.py and modules like tools.py, memory.py, and
#services/ollama_client.py
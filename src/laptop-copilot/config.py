# may later load defaults from models/

#What it does: Centralizes runtime settings.
#Logic used: Config loading logic from env variables, JSON files, defaults, and path
#resolution.
#Interconnection: Almost every other runtime file depends on this, especially services and
#startup code
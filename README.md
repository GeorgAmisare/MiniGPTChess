# MiniGPTChess

Server uses the OpenAI Responses API to select AI moves. Set the
``OPENAI_API_KEY`` environment variable before running the server. If the
API call fails or returns an invalid move, a random legal move is used.

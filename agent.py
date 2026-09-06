import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai import errors
from board import new_board, spawn_tile, game_over
from search import best_move
from tools import get_valid_moves, evaluate_board, directions

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

def generate_with_retry(model, contents, config, max_retries=4):
    delay = 20
    for attempt in range(max_retries):
        try:
            return client.models.generate_content(model=model, contents=contents, config=config)
        except errors.ClientError as e:
            if "429" in str(e) and attempt < max_retries - 1:
                print(f"Rate limited, waiting {delay}s before retry...")
                time.sleep(delay)
                delay *= 2
            else:
                raise

milestones = {128, 256, 512, 1024, 2048, 4096}

def check_milestone(board, seen_milestones) -> int | None:
    max_tile = max(max(row) for row in board)
    if max_tile not in seen_milestones and max_tile in milestones:
        seen_milestones.add(max_tile)
        return max_tile
    else:
        return None

def make_tools(board):
    def valid_moves_tool():
        return get_valid_moves(board)
    def eval_tool(direction):
        result = evaluate_board(board, direction)
        if result is None or result == float('-inf'):
            return "invalid or currently illegal move"
        return result
    return valid_moves_tool, eval_tool

valid_moves_declaration = types.FunctionDeclaration(
    name="get_valid_moves",
    description="Returns the list of legal move directions for the current 2048 board state.",
    parameters={
        "type": "object",
        "properties": {},
        "required": [],
    },
)

evaluate_board_declaration = types.FunctionDeclaration(
    name="evaluate_board",
    description="Scores how good the board would be after playing the given direction. Higher is better. Returns null if the direction" \
    " not currently legal.",
    parameters={
        "type": "object",
        "properties": {
            "direction": {
                "type": "string",
                "enum": ["left", "right", "up", "down"],
                "description": "The direction to evaluate.",
            }
        },
        "required": ["direction"],
    }
)

tool = types.Tool(function_declarations=[valid_moves_declaration, evaluate_board_declaration])

SYSTEM_PROMPT = '''
    You are playing 2048. A milestone tile was just reached, and you get to decide this one move. 
    Call get_valid_moves to see legal directions, then call evaluate_board on each legal direction to compare them
    (higher score is better)> Once you've decided, respond with a short explanation of your reasoning followed by a final
    line containing only one word: the chosen direction (left, right, up, down).
'''

def agent_choose_move(board, milestone):
    valid_moves_tool, eval_tool = make_tools(board)
    dispatch = {
        "get_valid_moves": valid_moves_tool,
        "evaluate_board": eval_tool,
    }

    user_message = f"You just reached the {milestone} tile. Decide your next move."
    contents = [types.Content(role="user", parts=[types.Part(text=user_message)])]

    while True:
        response = generate_with_retry(
            model="gemini-flash-lite-latest",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                tools=[tool],
                max_output_tokens=2048,
            )
        )
        part = response.candidates[0].content.parts[0]

        if part.function_call:
            call = part.function_call
            func = dispatch.get(call.name)
            result = func(**call.args)
            contents.append(response.candidates[0].content)
            contents.append(types.Content(
                role="user",
                parts=[types.Part.from_function_response(name=call.name, response={"result": result})]
            ))
        else:
            explanation = response.text
            lines = [line.strip() for line in explanation.strip().split("\n") if line.strip()]
            last_line = lines[-1].lower() if lines else ""
            direction = last_line if last_line in ["left", "right", "up", "down"] else None
            return direction, explanation

def play_with_agent(depth):
    board = new_board()
    seen_milestones = set()
    moves_played = 0

    while not game_over(board):
        milestone = check_milestone(board, seen_milestones)
        if milestone:
            time.sleep(5)
            direction, explanation = agent_choose_move(board, milestone)
            print(f"\nMILESTONE {milestone}!\n")
            print(explanation)
            move_fn = directions.get(direction) if direction else None
            if move_fn is None:
                move_fn = best_move(board, depth)
        else:
            move_fn = best_move(board, depth)

        board = move_fn(board)
        spawn_tile(board)
        moves_played += 1

    max_tile = max(max(row) for row in board)
    print(f"\nGame over. Max tile: {max_tile}, moves played: {moves_played}")
    return max_tile, moves_played
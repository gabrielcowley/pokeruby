# Create file 'egg_moves_input.txt' in this folder
# First line should be move name - eg 'MOVE_ANCIENT_POWER'
# Subsequent lines should be Pokemon name - eg 'DUNSPARCE'

import os
import re

input_path = os.path.join(os.path.dirname(__file__), 'egg_moves_input.txt')
egg_moves_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'data', 'pokemon', 'egg_moves.h')

def read_file(path: str) -> list[str]:
    result = []
    with open(path, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        result.append(line)
    return result

def overwrite_file(path: str, contents: str):
    with open(path, 'w') as f:
        f.write(contents)

def read_input() -> list[str]:
    return read_file(input_path)

def read_egg_moves() -> list[str]:
    return read_file(egg_moves_path)

def get_index_of_insertion(learnset_lines: list[str], pokemon: str) -> int:
    pokemon_start_pattern = rf'\s*?egg_moves\({pokemon},\s*?'
    pokemon_start_idx = -1
    for i in range(len(learnset_lines)):
        line = learnset_lines[i]
        match = re.fullmatch(pokemon_start_pattern, line)
        if match is not None:
            pokemon_start_idx = i
            break
    if pokemon_start_idx == -1:
        raise f'Pokemon {pokemon} not found'
    i = pokemon_start_idx + 1
    while (not learnset_lines[i].strip().endswith('),')):
        learnset_line = learnset_lines[i]
        if (len(learnset_line.strip()) == 0 or learnset_line.strip().startswith('egg_moves(')):
            raise f'Attempted to read start of next learnset at line {i + 1}, pokemon {pokemon}'
        i += 1
    return i
        
def get_lines_to_insert(new_move: str, line_to_insert_after: str) -> list[str]:
    line_to_insert_after_match = re.fullmatch(r'(\s*)(\w+)\),\s*?', line_to_insert_after)
    if line_to_insert_after_match is None:
        raise f'Line {line_to_insert_after} did not match insert after pattern'
    leading_whitespace = line_to_insert_after_match.group(1)
    move_to_insert_after = line_to_insert_after_match.group(2)
    first_line = f'{leading_whitespace}{move_to_insert_after},\n'
    second_line = f'{leading_whitespace}{new_move}),\n'
    return [first_line, second_line]

input_lines = read_input()
move = input_lines[0].strip()

learnset_lines = read_egg_moves()

insertion_idxs = []

for input_line_idx in range(1, len(input_lines)):
    pokemon = input_lines[input_line_idx].strip().upper()
    index_of_insertion = get_index_of_insertion(learnset_lines, pokemon)
    insertion_idxs.append(index_of_insertion)

insertions_sorted = sorted(insertion_idxs, reverse=True)

for insertion_idx in insertions_sorted:
    lines_to_insert = get_lines_to_insert(move, learnset_lines[insertion_idx])
    learnset_lines = learnset_lines[:insertion_idx] + lines_to_insert + learnset_lines[insertion_idx + 1:]

overwrite_file(egg_moves_path, ''.join(learnset_lines))

print('Success!')

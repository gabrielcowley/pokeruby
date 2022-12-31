# Create file 'level_up_learnset_input.txt' in this folder
# First line should be name of move - eg 'MOVE_PLAY_ROUGH'
# Subsequent lines should be Pokemon name and desired level separated by a comma - eg 'Persian,47'

import os
import re

input_path = os.path.join(os.path.dirname(__file__), 'level_up_learnset_input.txt')
level_up_learnsets_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'data', 'pokemon', 'level_up_learnsets.h')

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

def read_level_up_learnsets() -> list[str]:
    return read_file(level_up_learnsets_path)

def get_index_of_move_insertion(learnset_lines: list[str], pokemon: str, level: int) -> int:
    i = learnset_lines.index(f'const u16 g{pokemon}LevelUpLearnset[] = {{\n') + 1
    while (learnset_lines[i].strip() != 'LEVEL_UP_END'):
        learnset_line = learnset_lines[i]
        if (learnset_line.startswith('const u16')):
            raise f'Attempted to read start of next learnset at line {i + 1}, pokemon {pokemon}'
        level_up_move_match = re.fullmatch(r'\s*?LEVEL_UP_MOVE\( ?(\d+),.*?\),\s*?', learnset_line)
        if level_up_move_match is None:
            raise f'Unexpected input "{learnset_line}". Was expecting LEVEL_UP_MOVE format.'
        level_at_line = int(level_up_move_match.group(1))
        if level_at_line >= level:
            return i
        i += 1
    return i
        
def get_line_to_insert(pokemon: str, level: int, move: str, sample_with_leading_whitespace: str) -> str:
    leading_whitespace_match = re.fullmatch(r'(\s*)[^\s].*\n', sample_with_leading_whitespace)
    leading_whitespace = leading_whitespace_match.group(1)
    level_str = str(level)
    level_space = ' ' if len(level_str) < 2 else ''
    return f'{leading_whitespace}LEVEL_UP_MOVE({level_space}{level_str}, {move}),\n'

def is_level_at_insertion_already_full(learnset_lines: list[str], insertion_idx: int, level_to_insert: int) -> bool:
    pattern = rf'\s*?LEVEL_UP_MOVE\( ?{str(level_to_insert)},.*?\),\s*?'
    line_1_match = re.fullmatch(pattern, learnset_lines[insertion_idx])
    line_2_match = re.fullmatch(pattern, learnset_lines[insertion_idx + 1])
    line_3_match = re.fullmatch(pattern, learnset_lines[insertion_idx + 2])
    line_4_match = re.fullmatch(pattern, learnset_lines[insertion_idx + 3])
    return not (line_1_match is None or line_2_match is None or line_3_match is None or line_4_match is None)

input_lines = read_input()
move = input_lines[0].strip()

learnset_lines = read_level_up_learnsets()

move_insertions = {}
already_full_levels = []

for input_line_idx in range(1, len(input_lines)):
    [pokemon, level_str] = [x.strip() for x in input_lines[input_line_idx].split(',')]
    level_for_pokemon = int(level_str)
    index_of_move_insertion = get_index_of_move_insertion(learnset_lines, pokemon, level_for_pokemon)
    if is_level_at_insertion_already_full(learnset_lines, index_of_move_insertion, level_for_pokemon):
        already_full_levels.append(f'{pokemon}: level {level_str} is already full.')
    move_insertions[index_of_move_insertion] = (pokemon, level_for_pokemon)

if len(already_full_levels) > 0:
    print('\n'.join(already_full_levels))
else:
    move_insertions_it = iter(sorted(move_insertions.items(), reverse=True))

    while True:
        move_insertion = next(move_insertions_it, None)
        if move_insertion is None:
            break
        (move_insertion_idx, (pokemon, level)) = move_insertion
        line_to_insert = get_line_to_insert(pokemon, level, move, learnset_lines[move_insertion_idx])
        learnset_lines = learnset_lines[:move_insertion_idx] + [line_to_insert] + learnset_lines[move_insertion_idx:]

    overwrite_file(level_up_learnsets_path, ''.join(learnset_lines))

    print('Success!')

# Create file 'tmhm_learnset_input.txt' in this folder
# First line should be TM item name - eg 'TM45_ATTRACT'
# Subsequent lines should be Pokemon name - eg 'Bulbasaur'

import os
import re

input_path = os.path.join(os.path.dirname(__file__), 'tmhm_learnset_input.txt')
tmhm_learnsets_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'data', 'pokemon', 'tmhm_learnsets.h')

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

def read_tmhm_learnsets() -> list[str]:
    return read_file(tmhm_learnsets_path)

def get_index_of_tm_insertion(learnset_lines: list[str], pokemon: str, tm: str) -> int:
    pokemon_start_pattern = rf'\s*?\[{pokemon}\]\s+?=\s+?TMHM_LEARNSET\(.*\s*?'
    pokemon_start_idx = -1
    for i in range(len(learnset_lines)):
        line = learnset_lines[i]
        match = re.fullmatch(pokemon_start_pattern, line)
        if match is not None:
            pokemon_start_idx = i
            break
    if pokemon_start_idx == -1:
        raise f'Pokemon {pokemon} not found'
    tm_number = int(re.fullmatch(r'TM(\d+)_.*\s*?', tm).group(1))
    i = pokemon_start_idx
    while (len(learnset_lines[i].strip()) != 0):
        learnset_line = learnset_lines[i]
        if (learnset_line.strip().startswith('[') and not learnset_line.strip().startswith(f'[{pokemon}]')):
            raise f'Attempted to read start of next learnset at line {i + 1}, pokemon {pokemon}'
        existing_tmhm_match = re.fullmatch(r'.*(TM|HM)(\d+)_.*\s*?', learnset_line)
        if existing_tmhm_match is None:
            raise f'Unexpected input "{learnset_line}". Was expecting TMHM format.'
        tm_or_hm = existing_tmhm_match.group(1)
        if tm_or_hm == 'HM':
            return i
        existing_tm_number = int(existing_tmhm_match.group(2))
        if existing_tm_number >= tm_number:
            return i
        i += 1
    return i
        
def get_lines_to_insert(tm: str, sample: str, next_line: str, previous_line: str) -> (list[str], str):
    if sample.strip().startswith('['):
        idx_of_tmhm = sample.index('TMHM(')
        existing_tmhm = sample[idx_of_tmhm:].strip()
        first_line = sample[:idx_of_tmhm] + f'TMHM({tm})\n'
        second_line = next_line[:idx_of_tmhm] + f'{existing_tmhm}\n'
        return ([first_line, second_line], 'delete this')
    if len(sample.strip()) == 0:
        idx_of_tmhm = previous_line.index('TMHM(')
        first_line = f'{previous_line[:len(previous_line) - 3]}\n'
        second_line = previous_line[:idx_of_tmhm] + f'TMHM({tm})),\n'
        return ([first_line, second_line], 'delete previous')
    idx_of_tmhm = sample.index('TMHM(')
    return ([sample[:idx_of_tmhm] + f'TMHM({tm})\n'], 'keep')

input_lines = read_input()
tm = input_lines[0].strip()

learnset_lines = read_tmhm_learnsets()

tm_insertion_idxs = []

for input_line_idx in range(1, len(input_lines)):
    pokemon = f'SPECIES_{input_lines[input_line_idx].strip().upper()}'
    index_of_tm_insertion = get_index_of_tm_insertion(learnset_lines, pokemon, tm)
    tm_insertion_idxs.append(index_of_tm_insertion)

tm_insertions_sorted = sorted(tm_insertion_idxs, reverse=True)

for tm_insertion_idx in tm_insertion_idxs:
    (lines_to_insert, command) = get_lines_to_insert(tm, learnset_lines[tm_insertion_idx], learnset_lines[tm_insertion_idx + 1], learnset_lines[tm_insertion_idx - 1])
    if command == 'delete this':
        learnset_lines = learnset_lines[:tm_insertion_idx] + lines_to_insert + learnset_lines[tm_insertion_idx + 1:]
    elif command == 'delete previous':
        learnset_lines = learnset_lines[:tm_insertion_idx - 1] + lines_to_insert + learnset_lines[tm_insertion_idx:]
    else:
        learnset_lines = learnset_lines[:tm_insertion_idx] + lines_to_insert + learnset_lines[tm_insertion_idx:]

overwrite_file(tmhm_learnsets_path, ''.join(learnset_lines))

print('Success!')

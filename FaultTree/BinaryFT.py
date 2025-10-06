import os
import re
import random

def add_cost_to_fault_tree(input_file: str, output_file: str = None, random_max: float = 100):
    """
    Add a cost to each basic event in a fault tree file.

    Parameters:
        input_file (str): Path to the fault tree file
        output_file (str): Optional path to save the updated file
        random_max (float): Maximum random offset added to cost
    """
    if output_file is None:
        base, ext = os.path.splitext(input_file)
        output_file = f"{base}_with_cost{ext}"

    new_lines = []

    with open(input_file, "r") as f:
        for line in f:
            line_strip = line.strip()

            # Match basic events with probability: "X1" prob=0.1;
            match = re.match(r'(".*?")\s+prob=([\deE\+\-\.]+);', line_strip)
            if match:
                node, prob_str = match.groups()
                prob = float(prob_str)

                # Compute cost inversely proportional to probability + small random offset
                base_cost = 1.0 / prob
                cost = base_cost + random.uniform(0, random_max)
                cost_int = int(round(cost))

                new_line = f'{node} prob={prob_str} cost={cost_int};'
                new_lines.append(new_line)
            else:
                new_lines.append(line_strip)

    # **Write output to file**
    with open(output_file, "w") as f:
        f.write("\n".join(new_lines))

    print(f"✅ Costs added: {output_file}")

def make_binary_fault_tree_file(input_filename: str, output_filename: str):
    """
    Convert a fault tree file to binary form and save it to a new file.
    """
    with open(input_filename, "r") as f:
        ft_text = f.read()

    new_lines = []

    for line in ft_text.strip().splitlines():
        line = line.strip()

        # Keep toplevel, probabilities, and empty lines as-is
        if not line or 'prob=' in line or line.startswith('toplevel'):
            new_lines.append(line)
            continue

        # Match gates like: "X" and/or "A" "B" ...
        match = re.match(r'"(.*?)"\s+(and|or)\s+(.*);', line)
        if not match:
            new_lines.append(line)
            continue

        node, gate_type, children_str = match.groups()
        children = re.findall(r'"(.*?)"', children_str)

        # Already binary or unary → keep as is
        if len(children) <= 2:
            new_lines.append(line)
            continue

        # Rewrite to binary form with localized names
        aux_index = 1
        temp_lines = []
        while len(children) > 2:
            a, b = children[0], children[1]
            aux_name = f"{node}_bin{aux_index}"
            aux_index += 1
            temp_lines.append(f'"{aux_name}" {gate_type} "{a}" "{b}";')
            children = [aux_name] + children[2:]
        # Final gate connecting to root
        temp_lines.append(f'"{node}" {gate_type} "{children[0]}" "{children[1]}";')

        new_lines.extend(temp_lines)

    with open(output_filename, "w") as f:
        f.write("\n".join(new_lines))

    print(f"✅ Binary fault tree written to: {output_filename}")


def convert_all_fault_trees(input_folder: str, output_folder: str, file_extension: str = ".dft"):
    """
    Convert all fault tree files in input_folder to binary form and save them in output_folder.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for fname in os.listdir(input_folder):
        input_path = os.path.join(input_folder, fname)
        if os.path.isfile(input_path) and fname.endswith(file_extension):
            output_path = os.path.join(output_folder, fname)
            try:
                make_binary_fault_tree_file(input_path, output_path)
            except Exception as e:
                print(f"⚠️ Error processing {fname}: {e}")

def add_cost_to_all_fault_trees(input_folder: str, output_folder: str, file_extension: str = ".dft"):
    """
    Apply cost addition to all fault tree files in input_folder and save them to output_folder.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for fname in os.listdir(input_folder):
        input_path = os.path.join(input_folder, fname)
        if os.path.isfile(input_path) and fname.endswith(file_extension):
            output_path = os.path.join(output_folder, fname)
            try:
                add_cost_to_fault_tree(input_path, output_path)
            except Exception as e:
                print(f"⚠️ Error processing {fname}: {e}")


if __name__ == "__main__":
    input_folder = "FTexamples/FFORTbinary/"   # folder with original FTs
    output_folder = "FTexamples/FFORTbinarycost/"    # folder to save binary FTs

    add_cost_to_all_fault_trees(input_folder, output_folder)

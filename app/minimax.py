import json
import random
import collections
import itertools
import math


DIRECTIONS = {"u": "up", "d": "down", "l": "left", "r": "right"}
MAX_LEVEL = 5
X_CHANGE = {"up": 0, "down": 0, "left": -1, "right": 1}
Y_CHANGE = {"up": -1, "down": 1, "left": 0, "right": 0}
SCORES={"fruit": 10, "empty": 1, "wall": 1, "self": 2, "other_snake_dead": 2, "collision_other": 2, "starve": 1}

def get_move(data):
    print(json.dumps(data))
    tree = generate_tree(data)
    tree = evaluate_tree(data, tree)
    with open('tree.json', 'w') as f:
        f.write(json.dumps(root, indent=2))
    direction = max(tree.keys(), key=lambda x: tree[x].value)
    return DIRECTIONS[direction]

def generate_tree(data):
    tree = lambda: collections.defaultdict(tree)
    root = tree()
    all_combos = itertools.product(DIRECTIONS.keys(), repeat=MAX_LEVEL)
    for combo in all_combos:
        current = root
        for idx in range(len(combo)-1):
            direction = combo[idx]
            current = current[direction]
            current["value"] = 0
            current["is_min"] = bool(idx % 2)
            current["is_leaf"] = False
        else:
            current[direction] = dict(value=0, is_min=bool((idx+1) % 2), is_leaf=True)
    return root

def evaluate_tree(data, tree, head=None):
    head = head or data["you"]["body"][0]
    if tree["is_leaf"]:
        if data["you"]["health"] - MAX_LEVEL <= 0:
            tree["value"] = SCORES["starve"] * (data["you"]["health"] - MAX_LEVEL)
            return tree
        if head["x"] < 0
            tree["value"] = SCORES["wall"] * head["x"]
            return tree
        if head["y"] < 0
            tree["value"] = SCORES["wall"] * head["y"]
            return tree
        if head["x"] >= data["board"]["width"]
            tree["value"] = -SCORES["wall"] * head["x"]
            return tree
        if head["y"] >= data["board"]["height"]
            tree["value"] = -SCORES["wall"] * head["y"]
            return tree
        if head in data["you"]["body"]:
            tree["value"] = -SCORES["self"]
            return tree
        if head in data["board"]["food"]:
            tree["value"] = SCORES["fruit"] - math.sqrt((head["x"] - data["you"]["body"][0]["x"])**2 + (head["y"] - data["you"]["body"][0]["y"])**2)
            return tree
        if head in [snake["body"][0] for snake in data["board"]["snakes"] if (len(snake["body"]) < len(data["you"]["body"]))]:
            tree["value"] = SCORES["other_snake_dead"]
            return tree
        if head in [item for snake in data["board"]["snakes"] for item in snake["body"]]:
            tree["value"] = -SCORES["collision_other"]
            return tree
        tree["value"] = SCORES["empty"]
        return tree

    for direction in DIRECTIONS.keys():
        new_head=dict(x=head["x"] + X_CHANGE[direction], y=head["y"] + Y_CHANGE[direction])
        

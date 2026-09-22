import random


def random_pair(n_list, q_list, rng=None):
    generator = rng or random
    return generator.choice(n_list), generator.choice(q_list)


def random_choice(n_list, q_list, rng=None):
    name, question = random_pair(n_list, q_list, rng)
    return f"Question for **{name}**: {question}"
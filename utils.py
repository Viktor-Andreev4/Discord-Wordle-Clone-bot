import nextcord
import constants
import random
from typing import List, Optional


words = open("wordlist.txt").read().splitlines()

def generate_wordle_embed(user: nextcord.User, id: int) -> nextcord.Embed:
    embed = nextcord.Embed(title="Wordle")
    embed.description = "\n".join([generate_blanks()] * 6)
    embed.set_author(name=user.name, icon_url=user.display_avatar.url)
    embed.set_footer(text=
        f"ID: {id} | To play, type /play\n"
        "To guess, reply to this message."
    )
    return embed

def generate_blanks() -> str:
    return "\N{BLACK SQUARE BUTTON}" * 5

def is_valid_word(word: str) -> bool:
    return word.lower() in words

def random_wordle_id() -> int:
    return random.randint(0, len(words) - 1)

def generate_color_word(guess: str, answer: str) -> str:
    colored_word = [constants.EMOJI_CODES["gray"][letter] for letter in guess]
    answer_letters: List[Optional[str]] = list(answer)
    guess_letters: List[Optional[str]] = list(guess)
    for i in range(len(guess_letters)):
        if guess_letters[i] == answer_letters[i]:
            colored_word[i] = constants.EMOJI_CODES["green"][guess_letters[i]]
            answer_letters[i] = None
            guess_letters[i] = None

    for i in range(len(guess_letters)):
        if guess_letters[i] is not None and guess_letters[i] in answer_letters:
            colored_word[i] = constants.EMOJI_CODES["yellow"][guess_letters[i]]
            answer_letters[answer_letters.index(guess_letters[i])] = None

   
    return "".join(colored_word)

def update_embed(embed: nextcord.Embed, message: nextcord.Message) -> nextcord.Embed:
    guess = message.content
    user_id = message.author.id

    wordle_id = int(embed.footer.text.split()[1])
    answer = words[wordle_id]
    colored_word = generate_color_word(guess, answer)
    empty = generate_blanks()

    embed.description = embed.description.replace(empty, colored_word, 1)
    num_empty_slots = embed.description.count(empty)

    if guess == answer:
        if num_empty_slots == 0:
            embed.description += "\n\nPhew!"
        if num_empty_slots == 1:
            embed.description += "\n\nGreat!"
        if num_empty_slots == 2:
            embed.description += "\n\nSplendid!"
        if num_empty_slots == 3:
            embed.description += "\n\nImpressive!"
        if num_empty_slots == 4:
            embed.description += "\n\nMagnificent!"
        if num_empty_slots == 5:
            embed.description += "\n\nGenius!"
    elif num_empty_slots == 0:
        embed.description += f"\n\nThe answer was {answer}!"


    return embed


def is_game_over(embed: nextcord.Embed) -> bool:
    return "\n\n" in embed.description


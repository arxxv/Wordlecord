from functools import partial
from math import ceil
import random
from re import X
from discord import Interaction
import nextcord
import time
import os
import psycopg2

popwords = open('pop.txt').read()
popwords = popwords.split('\n')
N = len(popwords)
allwords = set([w.strip() for w in open('allwords.txt')])

conn = psycopg2.connect(os.environ['DATABASE_URL'])

EMOJI = {
    "yellow": {'a': '<:ya:939499195688157255>', 'b': '<:yb:939499196359266324>', 'c': '<:yc:939499196187291719>', 'd': '<:yd:939499196246020177>', 'e': '<:ye:939499196019519568>', 'f': '<:yf:939499195797233726>', 'g': '<:yg:939499196187299860>', 'h': '<:yh:939499196208254986>', 'i': '<:yi:939499196199874580>', 'j': '<:yj:939499196258598912>', 'k': '<:yk:939499196174704650>', 'l': '<:yl:939499196384419850>', 'm': '<:ym:939499196157923349>',
               'n': '<:yn:939497135383146506>', 'o': '<:yo:939499196363456512>', 'p': '<:yp:939499195935633410>', 'q': '<:yq:939497135395733594>', 'r': '<:yr:939499196413804625>', 's': '<:ys:939499196279558154>', 't': '<:yt:939497135248928800>', 'u': '<:yu:939499196388634714>', 'v': '<:yv:939499196757737503>', 'w': '<:yw:939499195893702739>', 'x': '<:yx:939499196556394566>', 'y': '<:yy:939497135391518720>', 'z': '<:yz:939499196417966080>'}, "green": {'a': '<:gra:939490308830408714>', 'b': '<:grb:939490308989796362>', 'c': '<:grc:939490309031747634>', 'd': '<:grd:939490308989788264>', 'e': '<:gre:939490309157580830>', 'f': '<:grf:939490308964646934>', 'g': '<:grg:939490309107253269>', 'h': '<:grh:939490309446987816>', 'i': '<:gri:939490309195313192>', 'j': '<:grj:939490309455347762>', 'k': '<:grk:939490308998180885>', 'l': '<:grl:939490309405016094>', 'm': '<:grm:939490309388263486>',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                       'n': '<:grn:939490309367275591>', 'o': '<:gro:939490309333725254>', 'p': '<:grp:939490309488926740>', 'q': '<:grq:939490309480538144>', 'r': '<:grr:939490309505699910>', 's': '<:grs:939490309845434388>', 't': '<:grt:939490309333741618>', 'u': '<:gru:939490309409234964>', 'v': '<:grv:939490309467959306>', 'w': '<:grw:939490309497307206>', 'x': '<:grx:939490309342101554>', 'y': '<:gry:939490309333741568>', 'z': '<:grz:939490309556027422>'}, "gray": {'a': '<:ga:939490395413426176>', 'b': '<:gb:939490395400839178>', 'c': '<:gc:939490395128221697>', 'd': '<:gd:939490395048542229>', 'e': '<:ge:939490395161763940>', 'f': '<:gf:939490395010760754>', 'g': '<:gg:939490395056910337>', 'h': '<:gh:939490394851393558>', 'i': '<:gi:939490395287605258>', 'j': '<:gj:939490395241476126>', 'k': '<:gk:939490394914324551>', 'l': '<:gl:939490395010760717>', 'm': '<:gm:939490395195314177>',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           'n': '<:gn:939490395329527858>', 'o': '<:go:939490395237269545>', 'p': '<:gp:939490394700398605>', 'q': '<:gq:939490395124023296>', 'r': '<:gr:939490395480547328>', 's': '<:gs:939490395392458773>', 't': '<:gt:939490395157565460>', 'u': '<:gu:939490395312771112>', 'v': '<:gv:939490394998194186>', 'w': '<:gx:939490395136598067>', 'x': '<:gw:939490395413418004>', 'y': '<:gy:939497269202407474>', 'z': '<:gz:939497269298872350>'}, "nums": {
        1: "<:num1:940297024555872309>",
        2: "<:num2:940297025205973022>",
        3: "<:num3:940297120777371698>",
        4: "<:num4:940297025205993522>",
        5: "<:num5:940297025218568203>",
        6: "<:num6:940297121058398301>",
        "F": ":thumbsdown:"
    }
}


base_dict = "https://www.dictionary.com/browse/"
keyboardOrder = {0: ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
                 1: ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
                 2: ['z', 'x', 'c', 'v', 'b', 'n', 'm']
                 }

blueEmoji = ':regional_indicator_'


def convert_to_preferred_format(sec):
    sec = sec % (24 * 3600)
    hour = sec // 3600
    sec %= 3600
    min = sec // 60
    sec %= 60
    return "%02d:%02d:%02d" % (hour, min, sec)


def generate_keyboard(keyboard=[], wrong=[], correct=[], partial=[]):
    if len(keyboard) == 0:
        for i in range(3):
            t = []
            for j in keyboardOrder[i]:
                t.append(blueEmoji+j+":")
            keyboard.append(t)

    else:
        for i in wrong:
            i1, i2 = 0, 0
            for j in range(3):
                if i in keyboardOrder[j]:
                    i1 = j
                    i2 = keyboardOrder[j].index(i)
                    break
            keyboard[i1][i2] = EMOJI['gray'][i]

        for i in partial:
            i1, i2 = 0, 0
            for j in range(3):
                if i in keyboardOrder[j]:
                    i1 = j
                    i2 = keyboardOrder[j].index(i)
                    break
            keyboard[i1][i2] = EMOJI['yellow'][i]

        for i in correct:
            i1, i2 = 0, 0
            for j in range(3):
                if i in keyboardOrder[j]:
                    i1 = j
                    i2 = keyboardOrder[j].index(i)
                    break
            keyboard[i1][i2] = EMOJI['green'][i]

    # return "\n".join(keyb)
    return keyboard


def get_keyboard_string(keyboard):
    lvls = []
    for i in range(3):
        t = " "*i*2
        for j in keyboard[i]:
            t += j+" "
        lvls.append(t)
    return "\n".join(lvls)


def keyboard_helper(guess, ans):
    wrong = []
    partial = []
    correct = []
    for i in range(len(guess)):
        if guess[i] == ans[i]:
            correct.append(guess[i])
        elif guess[i] in ans:
            partial.append(guess[i])
        else:
            wrong.append(guess[i])
    return wrong, partial, correct


def generate_embed(user, ansid):
    embed = nextcord.Embed(title="Play Wordle")
    embed.description = "\n".join(["\N{WHITE MEDIUM SQUARE}"*5]*6)
    embed.set_author(name=user.name, icon_url=user.display_avatar.url)
    keyboard = generate_keyboard()
    keybstr = get_keyboard_string(keyboard)
    embed.add_field(name="Keys:", value=keybstr, inline=False)
    embed.add_field(name="start", value=time.time(), inline=False)
    embed.set_footer(
        text=f"ID: {ansid} | To play, use the command /play\nTo guess, reply to this message with a word")
    return embed


def generate_leaderboard_embed():
    embed = nextcord.Embed(title="Leaderboard")

    cur = conn.cursor()
    cur.execute(
        "SELECT username FROM wordle GROUP BY username ORDER BY AVG(score) ASC LIMIT 3")
    leaders = cur.fetchall()

    embed.description = ""
    if len(leaders) > 0:
        embed.description += f"""\n:first_place: {leaders[0][0]}"""
    if len(leaders) > 1:
        embed.description += f"""\n\n:second_place: {leaders[1][0]}"""
    if len(leaders) > 2:
        embed.description += f"""\n\n:third_place: {leaders[2][0]}"""

    return embed


def is_valid_word(word):
    return word.lower() in allwords


def get_wordle_id():
    return random.randint(0, N-1)


def get_next_line(guess, ans):
    guess = guess.lower()
    nextline = [EMOJI["gray"][i] for i in guess]
    answer_letters, guess_letters = list(ans), list(guess)

    for i in range(len(guess)):
        if guess[i] == ans[i]:
            nextline[i] = EMOJI["green"][guess[i]]
            answer_letters[i] = None
            guess_letters[i] = None

    for i in range(len(guess)):
        if guess_letters[i] is not None and guess[i] in answer_letters:
            nextline[i] = EMOJI["yellow"][guess[i]]
            answer_letters[answer_letters.index(guess[i])] = None

    return "".join(nextline)


def game_over(embed):
    return "\n\n\n" in embed.description


def get_answer(ans):
    ansarr = []
    for i in ans:
        ansarr.append(EMOJI['green'][i])
    return ''.join(ansarr)


def update_embed(guess, embed):
    guess = guess.lower()
    ansid = int(embed.footer.text.split()[1])
    ans = popwords[ansid]
    nextline = get_next_line(guess, ans)
    empty_slot = "\N{WHITE MEDIUM SQUARE}" * 5
    embed.description = embed.description.replace(empty_slot, nextline, 1)
    keyboardstr = embed.fields[0].value
    keyboard = [i.split() for i in keyboardstr.split('\n')]
    wrong, partial, correct = keyboard_helper(guess, ans)
    keyboard = generate_keyboard(keyboard, wrong, correct, partial)
    keyboardstr = get_keyboard_string(keyboard)
    embed.set_field_at(0, name="Keys", value=keyboardstr, inline=False)
    guessesLeft = embed.description.count(empty_slot)

    url = base_dict+ans
    if guess == ans:
        if guessesLeft == 0:
            embed.description += "\n\n\nPhew!"
        if guessesLeft == 1:
            embed.description += "\n\n\nGood!"
        if guessesLeft == 2:
            embed.description += "\n\n\nGreat!"
        if guessesLeft == 3:
            embed.description += "\n\n\nImpressive!"
        if guessesLeft == 4:
            embed.description += "\n\n\nMagnificient!"
        if guessesLeft == 5:
            embed.description += "\n\n\nGenius!"
        embed.description += f'\n{get_answer(ans)}: {url}'
        embed.add_field(name="Took: ", value=convert_to_preferred_format(
            time.time()-int(embed.fields[1].value.split('.')[0])), inline=False)

        cur = conn.cursor()
        cur.execute(
            f"INSERT INTO wordle(username, score) values ('{embed.author.name}', {6-guessesLeft})")
        conn.commit()

    elif guessesLeft == 0:
        embed.description += f"\n\n\nIt was {get_answer(ans)}: {url}\nPlay Again?"
        cur = conn.cursor()
        cur.execute(
            f"INSERT INTO wordle(username, score) values ('{embed.author.name}', {0})")
        conn.commit()

    return embed

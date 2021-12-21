import datetime
import database
from config import postgresql_pool

welcome = "Welcome to the poll app!\n"

new_option_prompt = "Enter new option (or leave empty to stop adding options): "

def prompt_create_poll():
    title = input("enter poll's title: ")
    owner = input("enter poll's owner: ")
    options = []
    
    while new_option := input(new_option_prompt):
        options.append(new_option)

    database.create_poll(title, owner, options)

def list_all_polls():
    polls = database.get_all_polls()
    for _id, title, owner, ts in polls:
        ts = datetime.datetime.fromtimestamp(ts).strftime('%d.%m.%Y %H:%M')
        print(f"{_id} poll with title '{title}' (created by {owner} at {ts})")

def print_poll_options(poll_with_option: list[database.PollwithOption]):
    print(f"poll '{poll_with_option[0][1]}' with option:")
    for *head, option_id, option_text, _ in poll_with_option:
        print(f"{option_id}: {option_text}")

def prompt_poll_and_options():
    poll_id = input("enter poll id: ")
    poll = database.get_poll_options(poll_id)
    print_poll_options(poll)

def prompt_vote_poll():
    print("Here all polls for vote:")
    list_all_polls()
    poll_id = int(input("===============\nenter poll id for vote: "))
    poll = database.get_poll_options(poll_id)
    print_poll_options(poll)
    option = input("enter option id for vote: ")
    username = input("enter username who vote: ")
    database.add_vote(option, username)

def show_poll_votes():
    print("Here all polls for vote:")
    list_all_polls()
    poll_id = int(input("===============\nenter poll to view votes results: "))
    poll = database.get_poll_and_vote_results(poll_id)

    print(f"\n==========\nresults for '{poll[0][0]}'")

    for *head, option_text, vote_count, vote_persant in poll:
        print(f"{option_text} - {vote_count} votes ({vote_persant:.2f}% of all)")
    


def randomize_poll_winner():
    pass

menu_options = {
    "1": prompt_create_poll,
    "2": list_all_polls,
    "3": prompt_poll_and_options,
    "4": prompt_vote_poll,
    "5": show_poll_votes,
    "6": randomize_poll_winner
}

menu_prompt = """-- Menu --

1) Create new poll
2) List open polls
3) Show poll and options
4) Vote on a poll
5) Show poll votes
6) Select a random winner from a poll option
7) Exit

Enter your choice: """

def menu():

    print(welcome)
    database.create_tables()

    while (selection := input(menu_prompt)) != "7":
        try:
            menu_options[selection]()
        except KeyError:
            print("invalid input. Try again")
    
    if postgresql_pool:
        postgresql_pool.closeall
    print("Пул соединений PostgreSQL закрыт")



# ===========================================================

menu()



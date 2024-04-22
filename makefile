#Define the default target
all: game

#Define the game target
game:
    #Check if OS environment variable equals Windows_NT
	if [ "$(OS)" = "Windows_NT" ]; then \
		python game.py; \
	else \
		python3 game.py; \
	fi
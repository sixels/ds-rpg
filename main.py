from game import Game


if __name__ == "__main__":
    try:
        Game().start()
    except (KeyboardInterrupt, EOFError):
        pass

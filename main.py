from game import Game

if __name__ == "__main__":
    game = Game()

    try:
        game.start()
    except Exception as e:
        print(f"[CRASH] Game crashed, exception: {e}")
        game.quit()
    
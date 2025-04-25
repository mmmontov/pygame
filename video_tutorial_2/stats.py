

class Stats():
    """отслеживание статистики"""

    def __init__(self):
        self.run_game = True

        with open('best_score.txt', 'r', encoding='utf-8') as file:
            self.best_score = int(file.read())

    def reset_stats(self):
        """статистика изменяющаяся во время игры"""
        self.guns_left = 2
        self.score = 0

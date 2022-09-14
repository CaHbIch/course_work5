from unit import BaseUnit


class BaseSingleton(type):
    """ Базовый класс"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    """ Поле боя"""
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = False

    def __init__(self, battle_result):
        self.battle_result = battle_result

    def start_game(self, player: BaseUnit, enemy: BaseUnit):
        """ Начало игры"""
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self):
        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self.battle_result = "В этой битве нет победителя!"
        return self._end_game()
        if self.player.hp <= 0:
            self.battle_result = "Игрок проиграл битву!"
        return self._end_game()
        if self.enemy.hp <= 0:
            self.battle_result = "Игрок выиграл битву!"
        return self._end_game()

    def _stamina_regeneration(self):
        """ Востановление стамины"""
        if self.player.stamina + self.STAMINA_PER_ROUND > self.player.unit_class.max_stamina:
            self.player.stamina = self.player.unit_class.max_stamina
        elif self.player.stamina < self.player.unit_class.max_stamina:
            self.player.stamina += self.STAMINA_PER_ROUND
        if self.enemy.stamina + self.STAMINA_PER_ROUND > self.enemy.unit_class.max_stamina:
            self.enemy.stamina = self.enemy.unit_class.max_stamina
        elif self.enemy.stamina < self.enemy.unit_class.max_stamina:
            self.enemy.stamina += self.STAMINA_PER_ROUND

    def next_turn(self):
        """ следующий раунд"""
        result = self._check_players_hp()
        if result:
            return result
        if self.game_is_running:
            self._stamina_regeneration()
            self.player.stamina = round(self.player.stamina, 1)
            self.enemy.stamina = round(self.enemy.stamina, 1)
            self.player.hp = round(self.player.hp, 1)
            self.enemy.hp = round(self.enemy.hp, 1)
        return self.enemy.hit(self.player)

    def _end_game(self) -> str:
        """ Конец игры"""
        _instances = {}
        self.game_is_running = False
        return self.battle_result

    def player_hit(self) -> str:
        """ попадание игрока"""
        result = self.player.hit(self.enemy)
        return f"{result}\n{self.next_turn()}"

    def player_use_skill(self) -> str:
        """ Использует скилла играком"""
        result = self.player.use_skill(self.enemy)
        return f"{result}\n{self.next_turn()}"

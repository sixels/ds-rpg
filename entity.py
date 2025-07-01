class Entity:
    def get_total_health(self) -> int:
        """Retorna a vida total."""
        raise NotImplementedError

    def get_current_health(self) -> int:
        """Retorna a vida atual."""
        raise NotImplementedError

    def take_damage(self, damage: int):
        """Reduz a vida pelo dano recebido."""
        raise NotImplementedError

    def attack(self, other: "Entity") -> int:
        """Realiza um ataque e retorna o dano causado."""
        raise NotImplementedError

    def is_alive(self) -> bool:
        """Verifica se ainda está vivo."""
        return self.get_current_health() > 0

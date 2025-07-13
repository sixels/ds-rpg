from typing import Optional, Any
from enum import Enum


class ActionType(Enum):
    MOVE = "mover"
    STORE = "guardar"
    DROP = "remover"
    USE_POTION = "usar poção"
    EQUIP = "equipar"
    ATTACK = "atacar"
    SHOW_HELP = "ajuda"
    SHOW_BACKPACK = "mostrar mochila"
    SHOW_BELT = "mostrar cinto"


STOPWORDS = {"a", "o", "ao", "à", "em", "no", "na", "do", "da", "para"}

DEFAULT_ACTIONS: list[tuple[list[str], dict[str, Any], str]] = [
    # Ações de movimento
    (
        ["ir", "<direction>"],
        {"action": ActionType.MOVE},
        "Move-se na direção especificada",
    ),
    (
        ["mover", "<direction>"],
        {"action": ActionType.MOVE},
        "Move-se na direção especificada",
    ),
    (
        ["norte"],
        {"action": ActionType.MOVE, "direction": "norte"},
        "Move-se para o norte",
    ),
    (["sul"], {"action": ActionType.MOVE, "direction": "sul"}, "Move-se para o sul"),
    (
        ["leste"],
        {"action": ActionType.MOVE, "direction": "leste"},
        "Move-se para o leste",
    ),
    (
        ["oeste"],
        {"action": ActionType.MOVE, "direction": "oeste"},
        "Move-se para o oeste",
    ),
    #
    # Ações de pegar e organizar itens
    (
        ["guardar", "<item>", "<in>"],
        {"action": ActionType.STORE},
        "Guarda um item na mochila ou cinto",
    ),
    (
        ["colocar", "<item>", "<in>"],
        {"action": ActionType.STORE},
        "Guarda um item na mochila ou cinto",
    ),
    (
        ["tirar", "<item>", "<from>"],
        {"action": ActionType.DROP},
        "Remove um item do cinto ou mochila",
    ),
    (
        ["retirar", "<item>", "<from>"],
        {"action": ActionType.DROP},
        "Remove um item do cinto ou mochila",
    ),
    (
        ["remover", "<item>", "<from>"],
        {"action": ActionType.DROP},
        "Remove um item do cinto ou mochila",
    ),
    (
        ["olhar", "mochila"],
        {"action": ActionType.SHOW_BACKPACK},
        "Mostra a mochila",
    ),
    (
        ["mostrar", "mochila"],
        {"action": ActionType.SHOW_BACKPACK},
        "Mostra a mochila",
    ),
    (
        ["abrir", "mochila"],
        {"action": ActionType.SHOW_BACKPACK},
        "Mostra a mochila",
    ),
    (
        ["olhar", "cinto"],
        {"action": ActionType.SHOW_BELT},
        "Mostra o cinto",
    ),
    (
        ["mostrar", "cinto"],
        {"action": ActionType.SHOW_BELT},
        "Mostra o cinto",
    ),
    #
    # Equipar ou usar itens
    (
        ["usar", "<item>"],
        {"action": ActionType.USE_POTION},
        "Usa uma poção",
    ),
    (
        ["beber", "<item>"],
        {"action": ActionType.USE_POTION},
        "Usa uma poção",
    ),
    (
        ["equipar", "<item>"],
        {"action": ActionType.EQUIP},
        "Equipa um item",
    ),
    #
    # Ações de ataque
    (
        ["atacar", "<target>"],
        {"action": ActionType.ATTACK, "target": "<target>"},
        "Ataca um alvo",
    ),
    (
        ["atacar"],
        {"action": ActionType.ATTACK, "target": "monstro"},
        "Ataca o monstro na sala",
    ),
    (
        ["atacar", "monstro"],
        {"action": ActionType.ATTACK, "target": "monstro"},
        "Ataca o monstro na sala",
    ),
    #
    # Ações variadas
    (
        ["ajuda"],
        {"action": ActionType.SHOW_HELP},
        "Mostra a mensagem de ajuda",
    ),
]


class TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, "TrieNode"] = {}
        self.command: Optional[dict[str, Any]] = None
        self.is_wildcard: bool = False
        self.wildcard_name: Optional[str] = None


class Actions:
    def __init__(
        self, actions: list[tuple[list[str], dict[str, Any], str]] = DEFAULT_ACTIONS
    ) -> None:
        self.root: TrieNode = TrieNode()
        self.commands: list[tuple[str, dict[str, Any], str]] = []

        for pattern, command, hint in actions:
            self.insert(pattern, command, hint)

    def insert(
        self,
        pattern_tokens: list[str],
        command_template: dict[str, Any],
        hint: str = "",
    ) -> None:
        """
        Inserts a command pattern with optional wildcards like <item>, <target>, etc.
        """
        node = self.root
        for token in pattern_tokens:
            token = token.lower()
            if token.startswith("<") and token.endswith(">"):
                key = "<wildcard>"
                if key not in node.children:
                    node.children[key] = TrieNode()
                    node.children[key].is_wildcard = True
                    node.children[key].wildcard_name = token[1:-1]
                node = node.children[key]
            else:
                if token not in node.children:
                    node.children[token] = TrieNode()
                node = node.children[token]
        node.command = command_template.copy()
        self.commands.append((" ".join(pattern_tokens), command_template.copy(), hint))

    def show_help(self) -> str:
        """Returns a formatted string with the help message and all available commands."""
        help_text = "Comandos disponíveis:\n"
        for pattern, _, hint in self.commands:
            help_text += f"- {pattern} -> {hint}\n"
        return help_text.strip()

    def match(self, input_str: str) -> Optional[dict[str, Any]]:
        tokens = input_str.lower().split()
        return self._match_recursive(self.root, tokens, 0, {})

    def _match_recursive(
        self, node: TrieNode, tokens: list[str], index: int, wildcards: dict[str, str]
    ) -> Optional[dict[str, Any]]:
        if index == len(tokens):
            if node.command:
                resolved = dict(node.command)
                resolved.update(wildcards)
                return resolved
            return None

        token = tokens[index]

        if token in node.children:
            result = self._match_recursive(
                node.children[token], tokens, index + 1, wildcards.copy()
            )
            if result:
                return result

        if "<wildcard>" in node.children:
            wildcard_node = node.children["<wildcard>"]
            name = wildcard_node.wildcard_name

            for end in range(index + 1, len(tokens) + 1):
                value = " ".join(tokens[index:end])
                next_token = tokens[end] if end < len(tokens) else None

                if (
                    next_token in wildcard_node.children
                    or next_token in STOPWORDS
                    or next_token is None
                ):
                    new_wildcards = wildcards.copy()
                    new_wildcards[name] = self._clean_wildcard(value)
                    result = self._match_recursive(
                        wildcard_node, tokens, end, new_wildcards
                    )
                    if result:
                        return result

        return None

    def _clean_wildcard(self, value: str) -> str:
        """Remove stopwords from inside wildcard values (optional)."""
        return " ".join([w for w in value.split() if w not in STOPWORDS])


if __name__ == "__main__":
    trie = Actions()
    print(trie.show_help())

    assert trie.match("ir para norte") == {
        "action": ActionType.MOVE,
        "direction": "norte",
    }
    assert trie.match("sul") == {
        "action": ActionType.MOVE,
        "direction": "sul",
    }

    assert trie.match("guardar Espada de ferro na mochila") == {
        "action": ActionType.STORE,
        "item": "espada de ferro",
        "in": "mochila",
    }
    assert trie.match("colocar poção de cura no cinto") == {
        "action": ActionType.STORE,
        "item": "poção de cura",
        "in": "cinto",
    }
    assert trie.match("remover chave enferrujada do cinto") == {
        "action": ActionType.DROP,
        "item": "chave enferrujada",
        "from": "cinto",
    }

    assert trie.match("usar poção pequena") == {
        "action": ActionType.USE_POTION,
        "item": "poção pequena",
    }
    assert trie.match("equipar espada de madeira") == {
        "action": ActionType.EQUIP,
        "item": "espada de madeira",
    }

    assert trie.match("atacar esqueleto") == {
        "action": ActionType.ATTACK,
        "target": "esqueleto",
    }

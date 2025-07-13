"""Defi: https://pydefis.callicode.fr/defis/C22_GenList/txt"""
def main() -> None:
    """Main function."""
    def trouve_suite(ma_liste :list[int]) -> tuple[int, int]:
        """Identify edges of the first serie in ma_liste.
        - ma_liste: list to work with\n
        Return a tuple of first and last edge of the serie
        """
        entree = ma_liste[0]
        if len(ma_liste) == 1:
            return entree, entree

        next_value = ma_liste[0] + 1
        i = 1
        while ma_liste[i] == next_value:
            i += 1
            next_value += 1

        return entree, ma_liste[i - 1]

    with open("./pokedex/pokedex.txt") as f:
        poke = f.read()

    poke_list = poke.split(",")
    poke_list = list(map(int, poke_list))
    poke_list_trie = sorted(poke_list)

    resultat = ""
    while poke_list_trie:
        if poke_list_trie:
            entree, sortie = trouve_suite(poke_list_trie)
        else:
            sortie = entree

        if entree == sortie:
            resultat += f"{entree},"
        else:
            resultat += f"{entree}-{sortie},"

        print(resultat)
        if poke_list_trie:
            poke_list_trie = poke_list_trie[poke_list_trie.index(sortie) + 1:]

    resultat = resultat[:-1]
    print(f"Résultat = {resultat}")


if __name__ == "__main__":
    main()

import os
import sys

#implementace reTRIEval stromu v pythonu
#inspirováno geeksforgeeks.org
#autor: Filip Mironov, 239151

#samotný nod stromu má 2 atributy typu list
#první, Names, může obsahovat jakékoliv data základního datového typu string
#druhý, Nodes, odkazuje na na dceřiné nody
class TrieNode:
    def __init__(self):
        self.children_Names = []
        self.children_Nodes = []

#datová struktura je tímpádem tvořena z instancí classy TrieNode
#první nod je označen "root"
#dále je použita globální proměnná total_words, která v této verzi nemá smysl
#poslední globální proměnná complete_words je podstatná pro rekurzivní funkci browser_search
class TrieDatabase:
    def __init__(self):
        self.root = TrieNode()
        self.total_words = 0
        self.complete_words = []

    #první funkcí je zde přidání dat
    #návratem této funkce je bool zdar/nezdar, pro tuto verzi nepodstatné, jelikož interaktivní input s operátorem není realizován
    def insert(self, word):
        current_node = self.root
        insertion_succesful = False

        #cyklus v podstatě rozloží string na chary
        for i in range(len(word)):
            if word[i] not in current_node.children_Names:
                #pokud v se v dané úrovni struktury nenachází daný char, je přidán
                current_node.children_Names.append(word[i])
                new_node = TrieNode()
                current_node.children_Nodes.append(new_node)
                insertion_succesful = True
            #zde je vidět, jak je důležité, aby byly oba atributy Names a Nodes se stejným odpovídajícím indexem
            #nejprve najdeme pozici dalšího pomocí .index(word[i])
            #example:
            #pokud chceme přidat za sebou "matice", "matrix", "matika"
            #pro string matika musí pointer mezi t-i navazovat na správný index a nelze ho navázat na konec listu (r)
            next_node_position = current_node.children_Names.index(word[i])
            #poté se přesuneme na nový spodnější nod
            current_node = current_node.children_Nodes[next_node_position]

        if insertion_succesful == True:
            self.total_words += 1

        return insertion_succesful

    #jednoduchá funkce pro přidávání více stringů najednou
    #přidána kvůli mojí lenosti
    def insert_multiple(self, words):
        for i in range(len(words)):
            self.insert(words[i])

    #jednoduchá funkce na identifikaci, jestli se dané data v struktuře nachází
    #výstupem je bool
    def search(self, word):
        current_node = self.root
        search_succesful = False

        #stejně jako ve funkci insert se zde používá stejného principu
        for i in range(len(word)):
            if word[i] in current_node.children_Names:
                if i != len(word)-1:
                    next_node_position = current_node.children_Names.index(word[i])
                    current_node = current_node.children_Nodes[next_node_position]
                else:
                    search_succesful = True

        return search_succesful

    #funkce delete, pro odstanění dat ze struktury
    #mohou zde nastat 3 případy:
    #1. data jsou prefix jiných dat-nic se nemaže
    #2. data jsou v celém řetězci od rootu samostatná, maže se celý řetězec
    #3. data sdílejí prefix s jinými daty - např. matice a matematika
    def delete(self, word):
        current_node = self.root

        #funkcí search nejprve ověříme, jestli se data vůbec ve struktuře nachází
        deletion_possible = self.search(word)
        if deletion_possible == True:
            #int number_of_nodes trackuje kolik písmen se v každé spošlé úrovni nachází
            #example:
            #máme matrix a matice, chceme odstranit "matice"
            #první úroven ["m"] = 1
            #druhá úroven ["a"] = 1+1
            #třetí úroven ["t"] = 1+1+1
            #čtvrtá úroven ["r","i"] = 1+1+1+2
            #pátá úroven ["c"] = 1+1+1+2+1
            #...
            number_of_nodes = 0
            for i in range(len(word)):
                number_of_nodes += len(current_node.children_Names)
                next_node_position = current_node.children_Names.index(word[i])
                #klasika odkazů jako u search a insert
                previous_node = current_node
                current_node = current_node.children_Nodes[next_node_position]
            #stav 1 - je to prefix
            #další nod je větší, int number_of_nodes se zvetší
            number_of_nodes_plus_one = number_of_nodes + len(current_node.children_Names)
            #nic neměníme
            if number_of_nodes_plus_one > number_of_nodes:
                self.total_words -= 1
                pass
            #stav 2 a 3
            #pokud hodnota int number_of_nodes nestoupá, pomocí rekurze odděláváme poslední prvek z dat
            #pokud jde o stav 3, postupným odendáváním se splní podmínka 1 pro prefix a proces se ukončí
            #pokud jde o stav 2, celý řetězec se vymaže
            else:
                current_node = previous_node
                current_node.children_Nodes.pop(next_node_position)
                current_node.children_Names.pop(next_node_position)
                #usekávání řetězce
                word = word[:len(word)-1]
                #rekurze
                self.delete(word)

        return deletion_possible

    #poslední funkce je pro dokončování vyhledávání jako třeba našeptávač u internetových prohlížečů
    def browser_search(self, word):
        current_node = self.root

        #opět kontrola, jetli hledaný výraz vůbec existuje
        search_possible = self.search(word)
        if search_possible == True:
            #nejprve program dojde na konec zadaného výrazu
            for i in range(len(word)):
                next_node_position = current_node.children_Names.index(word[i])
                current_node = current_node.children_Nodes[next_node_position]
            #pokud za výrazem neleží další nody je přidán do globální proměnné complete_words
            if len(current_node.children_Names) == 0:
                self.complete_words.append(word)
            #pokud za výrazem leží, pomocí rekurze se na výraz nabalují další prvky, dokud nedojde ke kompletaci
            else:
                for j in range(len(current_node.children_Names)):
                    word_under_construction = word+current_node.children_Names[j]
                    self.browser_search(word_under_construction)
        return self.complete_words

    #nutná funkce pro vymazání globální proměnné
    def clear_browser_history(self):
        self.complete_words = []

    #funkce propojující dvě předchozí
    def use_browser(self, word):
        self.clear_browser_history()
        final = self.browser_search(word)
        return final


#main
if __name__ == '__main__':
    mojeDatabaze = TrieDatabase()

    mojeDatabaze.insert('matrix')
    mojeDatabaze.insert('matice')
    mojeDatabaze.insert('matematika')
    mojeDatabaze.insert_multiple(['Neo','Alien','Predator','123456'])

    print(mojeDatabaze.use_browser('mat'))
    print(mojeDatabaze.use_browser('Ne'))

    #mojeDatabaze.search('matrix')
    #mojeDatabaze.search('123456')

    mojeDatabaze.delete('matrix')
    mojeDatabaze.delete('mat')

    print(mojeDatabaze.use_browser('mat'))
# B+ tree in python
import math
import os
# Node creation
class Node:
    def __init__(self, order):
        self.order = order
        self.values = []
        self.keys = []
        self.nextKey = None
        self.parent = None
        self.check_leaf = False

    # Insert at the leaf
    def insert_at_leaf(self, value, key):
        key = str(key) 
        if self.values:
            for i in range(len(self.values)):
                if value == self.values[i]:
                    self.keys[i].append(key)
                    break
                elif value < self.values[i]:
                    self.values = self.values[:i] + [value] + self.values[i:]
                    self.keys = self.keys[:i] + [[key]] + self.keys[i:]
                    break
                elif i + 1 == len(self.values):
                    self.values.append(value)
                    self.keys.append([key])
                    break
        else:
            self.values = [value]
            self.keys = [[key]]
   
class Folder:
    def __init__(self, name):
        self.name = name
        self.files = []       # arquivos simples
        self.subfolders = {}  # nome -> Folder
        self.parent = None    # referência à pasta pai (se quiser navegar)

    def create_file(self, filename):
        if filename not in self.files:
            self.files.append(filename)
        else:
            print(f"Arquivo '{filename}' já existe.")

    def create_folder(self, foldername):
        if foldername not in self.subfolders:
            new_folder = Folder(foldername)
            new_folder.parent = self
            self.subfolders[foldername] = new_folder
        else:
            print(f"Pasta '{foldername}' já existe.")

    def list_contents(self):
        print(f"Conteúdo da pasta '{self.name}':")
        print(" Pastas:", list(self.subfolders.keys()))
        print(" Arquivos:", self.files)

# B plus tree
class BplusTree:
    def __init__(self, order):
        self.root = Node(order)
        self.order = order 
        self.root.check_leaf = True
        self.folder_map = {}
        #self.auto_key_counter = 1  
    def __str__(self):
        return "Árvore B+ com raiz contendo: " + str(self.root.values)
    def printTree(tree):
        queue = [(tree.root, 0)]
        current_level = 0
        print("B+ Tree structure:")
        while queue:
            node, level = queue.pop(0)
            if level > current_level:
                print()
                current_level = level
            print(f"[{', '.join(node.values)}]", end=" ")
            if not node.check_leaf:
                for child in node.keys:
                    queue.append((child, level + 1))
        print("\n")

    # Insert operation
    def insert(self, value, key):
        value = str(value)
        old_node = self.search(value)

    # Atualiza se já existe
        for i, v in enumerate(old_node.values):
            if v == value:
                old_node.keys[i].append(key)
                return

    # Insere valor novo
        old_node.insert_at_leaf(value, key)

    # Verifica se a folha ultrapassou o limite
        if len(old_node.values) > old_node.order:
        # Divide a folha ao meio
            mid = len(old_node.values) // 2

            new_leaf = Node(old_node.order)
            new_leaf.check_leaf = True
            new_leaf.parent = old_node.parent

        # Transfere metade dos valores para a nova folha
            new_leaf.values = old_node.values[mid:]
            new_leaf.keys = old_node.keys[mid:]
            old_node.values = old_node.values[:mid]
            old_node.keys = old_node.keys[:mid]

        # Atualiza ponteiros
            new_leaf.nextKey = old_node.nextKey
            old_node.nextKey = new_leaf

        # A chave promovida é a menor da nova folha
            promoted_key = new_leaf.values[0]

            self.insert_in_parent(old_node, promoted_key, new_leaf)

    # Search operation for different operations
    def search(self, value):
        value = str(value)
        current_node = self.root
        while not current_node.check_leaf:
            i = 0
            while i < len(current_node.values) and value >= current_node.values[i]:
                i += 1
            current_node = current_node.keys[i]
        return current_node
    
    # Find the node
    def find(self, value):
        value = str(value)
        leaf = self.search(value)  # Busca o nó folha onde o valor pode estar
        for i in range(len(leaf.values)):
            if leaf.values[i] == value:
                return True
        return False  # Só retorna False se não encontrar em nenhum lugar

    # Inserting at the parent
    def insert_in_parent(self, n, value, ndash):
        if (self.root == n):
            rootNode = Node(n.order)
            rootNode.values = [value]
            rootNode.keys = [n, ndash]
            self.root = rootNode
            n.parent = rootNode
            ndash.parent = rootNode
            return

        parentNode = n.parent
        temp3 = parentNode.keys
        for i in range(len(temp3)):
            if (temp3[i] == n):
                parentNode.values = parentNode.values[:i] + \
                    [value] + parentNode.values[i:]
                parentNode.keys = parentNode.keys[:i +
                                                  1] + [ndash] + parentNode.keys[i + 1:]
                if (len(parentNode.keys) > parentNode.order):
                    parentdash = Node(parentNode.order)
                    parentdash.parent = parentNode.parent
                    mid = int(math.ceil(parentNode.order / 2)) - 1
                    parentdash.values = parentNode.values[mid + 1:]
                    parentdash.keys = parentNode.keys[mid + 1:]
                    value_ = parentNode.values[mid]
                    if (mid == 0):
                        parentNode.values = parentNode.values[:mid + 1]
                    else:
                        parentNode.values = parentNode.values[:mid]
                    parentNode.keys = parentNode.keys[:mid + 1]
                    for j in parentNode.keys:
                        j.parent = parentNode
                    for j in parentdash.keys:
                        j.parent = parentdash
                    self.insert_in_parent(parentNode, value_, parentdash)

    
    
    # Delete a node
    
class SimuladorShell:
    def __init__(self):
        self.cwd = "/"  # diretório atual
        self.sistema = {"/": []}  # sistema de arquivos simulado
        self.auto_key_counter = 1

    def prompt(self):
        return f"simulador:{self.cwd}$ "

    def pwd(self):
        print(self.cwd)
    
    def mkdir(self, args):
        if not args:
            print("Uso: mkdir <nome>")
            return
        nome = args[0]
        caminho = os.path.join(self.cwd, nome).replace("\\", "/")
        if not caminho.endswith("/"):
            caminho += "/"
        if caminho in self.sistema:
            print("Diretório já existe.")
        else:
            self.sistema[caminho] = []
            self.sistema[self.cwd].append(nome + "/")
            chave = str(self.auto_key_counter)
            bpt.insert(nome, chave)
            print(f"Diretório '{nome}' criado com chave {chave}")
            self.auto_key_counter += 1
           

    def touch(self, args):
        if not args:
            print("Uso: touch <arquivo>")
            return
        nome = args[0]
        if nome in self.sistema[self.cwd]:
            print("Arquivo já existe.")
        else:
            self.sistema[self.cwd].append(nome)

    def ls(self):
        itens = self.sistema.get(self.cwd, [])
        for item in sorted(itens):
            print(item)

    def cd(self, args):
        if not args:
            self.cwd = "/"
            return
        nome = args[0]
        if nome == "..":
            if self.cwd != "/":
                self.cwd = "/".join(self.cwd.rstrip("/").split("/")[:-1]) + "/"
                if self.cwd == "":
                    self.cwd = "/"
        else:
            novo = os.path.join(self.cwd, nome).replace("\\", "/")
            if not novo.endswith("/"):
                novo += "/"
            if novo in self.sistema:
                self.cwd = novo
            else:
                print("Diretório não encontrado.")

    def rm(self, args):
        if not args:
            print("Uso: rm <nome>")
            return
        nome = args[0]
    
    # Aqui você deve obter a chave correta associada ao nome
    # Exemplo simples: usar uma chave fixa (ajuste para sua implementação)
        chave = 5  
    
        if nome + "/" in self.sistema[self.cwd]:
            caminho = os.path.join(self.cwd, nome).replace("\\", "/") + "/"
            if caminho in self.sistema:
                del self.sistema[caminho]
            self.sistema[self.cwd].remove(nome + "/")
            self.bpt.delete(nome, chave)  # chama remoção na B+ Tree
        elif nome in self.sistema[self.cwd]:
            self.sistema[self.cwd].remove(nome)
            self.bpt.delete(nome, chave)  # chama remoção na B+ Tree
        else:
            print("Arquivo ou diretório não encontrado.")

    




    def executar(self):
        while True:
            try:
                entrada = input(self.prompt()).strip()
                if not entrada:
                    continue

                partes = entrada.split()
                comando = partes[0]
                argumentos = partes[1:]

                if comando == "exit":
                    print("Saindo.")
                    break
                elif comando == "pwd":
                    self.pwd()
                elif comando == "mkdir":
                    self.mkdir(argumentos)
                elif comando == "ls":
                    self.ls()
                elif comando == "cd":
                    self.cd(argumentos)
                elif comando == "touch":
                    self.touch(argumentos)
                elif comando == "rm":
                    self.rm(argumentos)
                elif comando == "printTree":
                    printTree(bpt)
                else:
                    print(f"Comando não reconhecido: {comando}")

            except KeyboardInterrupt:
                print("\nUse 'exit' para sair.")
            except Exception as e:
                print(f"Erro: {e}")

def printTree(bpt):
    def print_node(node, level=0):
        indent = "  " * level
        print(f"{indent}Nó (folha={node.check_leaf}): {node.values}")
        if not node.check_leaf:
            for child in node.keys:
                print_node(child, level + 1)
    print("----- Estrutura da Árvore B+ -----")
    print_node(bpt.root)

bpt = BplusTree(order=4)

bpt.insert("Maria", 1)
bpt.insert("João", 2)
bpt.insert("Ana", 3)
bpt.insert("Carlos", 4)
bpt.insert("Beatriz", 5)
bpt.insert("Yan", 6)
bpt.insert("Tiago", 7)
bpt.insert("Roberto", 8)
bpt.insert("Bernardo", 9)
bpt.insert("Daniel", 10)

printTree(bpt)
#print(bpt)
'''
if bpt.find("Carlos"):
    print("find")
else:
    print("NOte found")
if bpt.find("Carlos"):
    print("Found")
else:
    print("Not found")
'''
if __name__ == "__main__":
    shell = SimuladorShell()
    shell.executar()

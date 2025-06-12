# main.py
import os
M = 3
import math

class Node:
    def __init__(self, order):
        self.order = order
        self.values = []
        self.keys = []
        self.nextKey = None
        self.parent = None
        self.check_leaf = False

    # Insert at the leaf
    def insert_at_leaf(self, leaf, value, key):
        if (self.values):
            temp1 = self.values
            for i in range(len(temp1)):
                if (value == temp1[i]):
                    self.keys[i].append(key)
                    break
                elif (value < temp1[i]):
                    self.values = self.values[:i] + [value] + self.values[i:]
                    self.keys = self.keys[:i] + [[key]] + self.keys[i:]
                    break
                elif (i + 1 == len(temp1)):
                    self.values.append(value)
                    self.keys.append([key])
                    break
        else:
            self.values = [value]
            self.keys = [[key]]
class BPlusTreeNode:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []
        self.parent = None
    
class BplusTree:
    def __init__(self, order):
        self.root = Node(order)
        self.root.check_leaf = True

    # Insert operation
    def insert(self, value, key):
        value = str(value)
        old_node = self.search(value)
        old_node.insert_at_leaf(old_node, value, key)

        if (len(old_node.values) == old_node.order):
            node1 = Node(old_node.order)
            node1.check_leaf = True
            node1.parent = old_node.parent
            mid = int(math.ceil(old_node.order / 2)) - 1
            node1.values = old_node.values[mid + 1:]
            node1.keys = old_node.keys[mid + 1:]
            node1.nextKey = old_node.nextKey
            old_node.values = old_node.values[:mid + 1]
            old_node.keys = old_node.keys[:mid + 1]
            old_node.nextKey = node1
            self.insert_in_parent(old_node, node1.values[0], node1)

    # Search operation for different operations
    def search(self, value):
        current_node = self.root
        while(current_node.check_leaf == False):
            temp2 = current_node.values
            for i in range(len(temp2)):
                if (value == temp2[i]):
                    current_node = current_node.keys[i + 1]
                    break
                elif (value < temp2[i]):
                    current_node = current_node.keys[i]
                    break
                elif (i + 1 == len(current_node.values)):
                    current_node = current_node.keys[i + 1]
                    break
        return current_node

    # Find the node
    def find(self, value, key):
        l = self.search(value)
        for i, item in enumerate(l.values):
            if item == value:
                if key in l.keys[i]:
                    return True
                else:
                    return False
        return False

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

class SimuladorShell:
    def __init__(self):
        self.cwd = "/"  # diretório atual
        self.sistema = {"/": []}  # sistema de arquivos simulado

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
            
        bplustree.insert(args)
    
    
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
                    print("mkdir")
                    self.mkdir(argumentos)
                elif comando == "ls":
                    print("ls")
                    self.ls()
                elif comando == "cd":
                    print("cd")
                    self.cd(argumentos)
                elif comando == "touch":
                    print("cdtouch")
                    self.touch(argumentos)
                elif comando == "rm":
                    print("rm")
                    self.rm(argumentos)
                elif comando == "printtree":
                    print("ok")
                    self.printTree(argumentos)
                else: 
                    print("Comando não existe!")
                
            except KeyboardInterrupt:
                print("\nUse 'exit' para sair.")
            except Exception as e:
                print(f"Erro: {e}")

record_len = 3
bplustree = BplusTree(record_len)
# Para rodar o simulador:
if __name__ == "__main__":
    shell = SimuladorShell()
    shell.executar()

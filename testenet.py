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
    '''
    def insert_at_leaf(self, value, key):
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
    
'''

# B plus tree
class BplusTree:
    def __init__(self, order):
        self.root = Node(order)
        self.root.check_leaf = True
        #self.auto_key_counter = 1  

    # Insert operation
    def insert(self, value, key):
        value = str(value)
        old_node = self.search(value)
        old_node.insert_at_leaf(value, key)
        print(value)
        print(key)

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
        value = str(value)
        key = str(key)
        l = self.search(value)
        for i, item in enumerate(l.values):
            if item == value:
                if key in l.keys[i]:
                    return True
                else:
                    return False
        return False
    '''
    def find(self, value, key):
        l = self.search(value)
        for i, item in enumerate(l.values):
            if item == value:
                if key in l.keys[i]:
                    return True
                else:
                    return False
        return False
    '''
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

    def delete(self, value, key):
        value = str(value)
        key = str(key)
        node_ = self.search(value)

        
        temp = 0
        for i, item in enumerate(node_.values):
            if item == value:
                


                if key in node_.keys[i]:
                    temp = 1
                    node_.keys[i].remove(key)

                # Se ainda há outras chaves associadas a esse value, nada mais a fazer
                    if len(node_.keys[i]) > 0:
                        return

                # Se não há mais nenhuma chave para esse value, remova o value
                    node_.values.pop(i)
                    node_.keys.pop(i)

                # Se for folha e root, pode parar
                    if node_ == self.root:
                        return

                # Inicia reestruturação
                    self.deleteEntry(node_, value)
                    return
        if temp == 0:
            print("Value not in Tree")
            return


    # Delete an entry
    def deleteEntry(self, node_, value):
        parent = node_.parent

    # Se root ficou vazio e tem apenas um filho, promove o filho a nova root
        if node_ == self.root and not node_.check_leaf and len(node_.keys) == 1:
            self.root = node_.keys[0]
            self.root.parent = None
            return

    # Se node_ está abaixo do mínimo, tentar redistribuir ou fundir
        min_values = math.ceil((node_.order - 1) / 2)
        if node_.check_leaf:
            if len(node_.values) >= min_values:
                return
        else:
            if len(node_.keys) >= math.ceil(node_.order / 2):
                return

    # Localizar irmãos
        idx = parent.keys.index(node_)
        left_sibling = parent.keys[idx - 1] if idx > 0 else None
        right_sibling = parent.keys[idx + 1] if idx + 1 < len(parent.keys) else None

    # Tentar redistribuição ou fusão
        if left_sibling and len(left_sibling.values) > min_values:
        # Move um elemento do irmão esquerdo
            if node_.check_leaf:
                value_moved = left_sibling.values.pop(-1)
                key_moved = left_sibling.keys.pop(-1)
                node_.values.insert(0, value_moved)
                node_.keys.insert(0, key_moved)
                parent.values[idx - 1] = node_.values[0]
            else:
                key_moved = left_sibling.keys.pop(-1)
                value_moved = parent.values[idx - 1]
                node_.keys.insert(0, key_moved)
                node_.values.insert(0, value_moved)
                parent.values[idx - 1] = left_sibling.values[-1]
            return

        elif right_sibling and len(right_sibling.values) > min_values:
        # Move um elemento do irmão direito
            if node_.check_leaf:
                value_moved = right_sibling.values.pop(0)
                key_moved = right_sibling.keys.pop(0)
                node_.values.append(value_moved)
                node_.keys.append(key_moved)
                parent.values[idx] = right_sibling.values[0]
            else:
                key_moved = right_sibling.keys.pop(0)
                value_moved = parent.values[idx]
                node_.keys.append(key_moved)
                node_.values.append(value_moved)
                parent.values[idx] = right_sibling.values[0]
            return

    # Fusão com irmão
        if left_sibling:
            if node_.check_leaf:
                left_sibling.values += node_.values
                left_sibling.keys += node_.keys
                left_sibling.nextKey = node_.nextKey
            else:
                left_sibling.values += [parent.values[idx - 1]] + node_.values
                left_sibling.keys += node_.keys
            parent.keys.pop(idx)
            parent.values.pop(idx - 1)
        elif right_sibling:
            if node_.check_leaf:
                node_.values += right_sibling.values
                node_.keys += right_sibling.keys
                node_.nextKey = right_sibling.nextKey
            else:
                node_.values += [parent.values[idx]] + right_sibling.values
                node_.keys += right_sibling.keys
            parent.keys.pop(idx + 1)
            parent.values.pop(idx)
    
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

    

# Print the tree
# Supondo que você já tenha suas classes Node e BplusTree aqui definidas...

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
1   
bpt = BplusTree(order=4)

bpt.insert("Maria", 1)
bpt.insert("João", 2)
bpt.insert("Ana", 3)
bpt.insert("Carlos", 4)
bpt.insert("Beatriz", 5)

printTree(bpt)

'''
bplustree.insert('15', '21')
bplustree.insert('25', '31')
bplustree.insert('35', '41')
bplustree.insert('45', '10')
'''

#printTree(bplustree)

if(bpt.find('Maria', '2')):
    print("Found")
else:
    print("Not found")

if __name__ == "__main__":
    shell = SimuladorShell()
    shell.executar()

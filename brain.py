import numpy as np
from scipy.special import softmax
import matplotlib.pyplot as plt
from copy import deepcopy

class Brain:

    OBSERVATIONS = ['light-up-left', 'light-up', 'light-up-right', 'light-left', 'light-right', 'light-down-left', 'light-down', 'light-down-right', 
          'organism-up-left', 'organism-up', 'organism-up-right', 'organism-left', 'organism-right', 'organism-down-left', 'organism-down', 'organism-down-right', 
          'time', 'energy']
    
    ACTIONS = ['up', 'down', 'left', 'right', 'photosynthesis', 'attack', 'reproduce']

    def __init__(self, genome=None, input_size=18, hidden_size=10, output_size=7, size=100):
        self.input_size = input_size # 8 light levels, 8 other organisms, 1 time, 1 energy
        self.hidden_size = hidden_size
        self.output_size = output_size # 4 movement, 1 photosynthesis, 1 attack, 1 reproduction

        if genome is None:
            genome = self.random_genome(size)
        self.genome = genome

        self.weights_layer1 = np.zeros((self.input_size, self.hidden_size))
        self.weights_layer2 = np.zeros((self.hidden_size, self.output_size)) 
        self.activation1 = np.tanh
        self.activation2 = softmax
        self.decipher()

    def random_genome(self, size):
        genome = []
        # gene: {'layer': 0-1, 'row': int, 'col': int, 'value': float}
        for i in range(size):
            gene = {}
            gene['layer'] = np.random.randint(0, 2)
            if gene['layer'] == 0:
                gene['row'] = np.random.randint(0, self.input_size)
                gene['col'] = np.random.randint(0, self.hidden_size)
            elif gene['layer'] == 1:
                gene['row'] = np.random.randint(0, self.hidden_size)
                gene['col'] = np.random.randint(0, self.output_size)
            gene['value'] = np.random.uniform(-1, 1)
            genome.append(gene)  
        return genome    

    def decipher(self):
        for gene in self.genome:
            if gene['layer'] == 0:
                self.weights_layer1[gene['row']][gene['col']] = gene['value']
            elif gene['layer'] == 1:
                self.weights_layer2[gene['row']][gene['col']] = gene['value']

    def get_action(self, state):
        input_layer = np.array(state)
        hidden_layer = self.activation1(np.dot(input_layer, self.weights_layer1))
        output_layer = self.activation2(np.dot(hidden_layer, self.weights_layer2))
        return output_layer.tolist().index(max(output_layer))     
    
    def mutate(self, mutation_rate):
        mutated_genome = []
        for gene in self.genome:
            mutated_gene = deepcopy(gene)
            for key in mutated_gene.keys():
                if np.random.uniform(0, 1) < mutation_rate:
                    if key == 'layer':
                        mutated_gene[key] = np.random.randint(0, 2)
                        if mutated_gene[key] == 0:
                            mutated_gene['row'] %= self.input_size 
                            mutated_gene['col'] %= self.hidden_size
                        elif mutated_gene[key] == 1:
                            mutated_gene['row'] %= self.hidden_size
                            mutated_gene['col'] %= self.output_size
                    elif key == 'row':
                        if mutated_gene['layer'] == 0:
                            mutated_gene[key] = np.random.randint(0, self.input_size)
                        elif mutated_gene['layer'] == 1:
                            mutated_gene[key] = np.random.randint(0, self.hidden_size)
                    elif key == 'col':
                        if mutated_gene['layer'] == 0:
                            mutated_gene[key] = np.random.randint(0, self.hidden_size)
                        elif mutated_gene['layer'] == 1:
                            mutated_gene[key] = np.random.randint(0, self.output_size)
                    elif key == 'value':
                        mutated_gene[key] = np.random.uniform(-1, 1)
            mutated_genome.append(mutated_gene)
        return mutated_genome

    def difference(self, other):
        difference = 0
        for gene1, gene2 in zip(self.genome, other.genome):
            for key in gene1.keys():
                if gene1[key] != gene2[key]:
                    difference += 1
        return difference / (len(self.genome) * 4)

    def genome_to_RGB(self):
        color = [0, 0, 0]
        for gene in self.genome:
            if gene['layer'] == 0:
                color[0] += gene['row'] / self.input_size
                color[1] += gene['col'] / self.hidden_size
            elif gene['layer'] == 1:
                color[0] += gene['row'] / self.hidden_size
                color[1] += gene['col'] / self.output_size
            color[2] += (gene['value'] + 1) / 2

        color = [(c / len(self.genome)) for c in color]
        print(color)
        return tuple(color)

    def visualize(self):
        plt.xlim(-2, 4)
        for i in range(self.input_size):
            plt.plot(0, i, 'o', color='black')
            plt.text(-0.25, i, self.OBSERVATIONS[i], fontsize=8, horizontalalignment='right')
        for i in range(self.hidden_size):
            plt.plot(1, 4 + i, 'o', color='black')
        for i in range(self.output_size):
            plt.plot(2, 5 + i, 'o', color='black')
            plt.text(2.25, 5 + i, self.ACTIONS[i], fontsize=8)

        for i in range(self.input_size):
            for j in range(self.hidden_size):
                if self.weights_layer1[i][j] != 0:
                    plt.plot([0, 1], [i, 4 + j], color='blue', linewidth=abs(self.weights_layer1[i][j]) * 2)


        for i in range(self.hidden_size):
            for j in range(self.output_size):
                if self.weights_layer2[i][j] != 0:
                    plt.plot([1, 2], [4 + i, 5 + j], color='blue', linewidth=abs(self.weights_layer2[i][j]) * 2)

        plt.show()


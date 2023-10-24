# -*- coding: utf-8 -*-
"""GeneticAlgorithm.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ng_nAih2F7SwZnxQbFm-hCMWsYCNBwLB

# Genetic Algorithm
###### Glorious Satria Dhamang Aji | 1302213015
###### Kevin | 1302210019

Finding the best minimum value of given function using Genetic Algorithm Implementation
"""

import random
from math import sin,cos,sqrt,exp

x1_batas = [-10,10]
x2_batas = [-10,10]

#Create the population and the cromosome
def generate_population(jumlah_individu, panjang_individu):
    return [[random.randint(0,9) for i in range(panjang_individu)] for j in range(jumlah_individu)]

# Generate the population
jumlah_individu = 20
panjang_individu = 6
population = generate_population(jumlah_individu, panjang_individu)

# Display the population
for individual in population:
    print(individual)

#Split cromosome into two part
def split_cromosome(kromosom):
    return kromosom[:len(kromosom)//2], kromosom[len(kromosom)//2:]

#decode cromosome
def decode(cromosome, batas):
   kali, pembagi = 0, 0
   for i in range(len(cromosome)) :
        num = cromosome[i]
        kali += num * (10**-(i+1))
        pembagi += 9 * (10**-(i+1))

   return batas[0] + (((batas[1] - batas[0]) / pembagi) * kali)

# Display the population and split chromosomes
for individual in population:
    print("Original Chromosome:", individual)

    kromosom_a, kromosom_b = split_cromosome(individual)

    print("Split Chromosome A:", kromosom_a)
    print("Split Chromosome B:", kromosom_b)

    decoded_x1 = decode(kromosom_a, x1_batas)
    decoded_x2 = decode(kromosom_b, x2_batas)

    print("Decoded x1:", decoded_x1)
    print("Decoded x2:", decoded_x2)
    print()

#rumus yang akan dicari nilai minimumnya
def function(x,y):
    return (sin(x)*cos(y)+0.8*exp(1-sqrt(x**2+y**2))) * -1

# Display the population and split chromosomes
for individual in population:
    print("Original Chromosome:", individual)

    kromosom_a, kromosom_b = split_cromosome(individual)

    print("Split Chromosome A:", kromosom_a)
    print("Split Chromosome B:", kromosom_b)

    decoded_x1 = decode(kromosom_a, x1_batas)
    decoded_x2 = decode(kromosom_b, x2_batas)

    print("Decoded x1:", decoded_x1)
    print("Decoded x2:", decoded_x2)

    objective_function_value = function(decoded_x1, decoded_x2)
    print("Objective Function : ", objective_function_value)

    fitness_value = 1 / (function(decoded_x1, decoded_x2)+0.0001)
    print("Fitness Value : ", fitness_value)


    print()

# Fungsi untuk menentukan kromosom terbaik
def best_kromosom_selection(population):
    min_fitness = 999
    min_kromosom = []

    for kromosom in population:
        kromosom_a, kromosom_b = split_cromosome(kromosom)
        x1 = decode(kromosom_a, x1_batas)
        x2 = decode(kromosom_b, x2_batas)
        fitness = function(x1, x2)

        if  min_fitness > fitness:
            min_fitness = fitness
            min_kromosom = kromosom

    return min_kromosom, min_fitness, x1, x2

best_population = best_kromosom_selection(population)

print("Best kromosom : ",best_population[0])
print("Best fitness  : " ,best_population[1])
print("Best decode x1: ",best_population[2])
print("Best decode x2: ",best_population[3])

# function to do the parent selection process
def parent_roulette_selection(population, fitness,fitness_total):
  probability = random.random()
  index_parent = 0
  while probability > 0:
    probability -= fitness[index_parent]/fitness_total
    index_parent += 1
    if index_parent == len(population) - 1:
      break

  return population[index_parent]

# crossover and breed new individuals
def crossover(orangtua1, orangtua2):
    anak1, anak2, anakan = [], [], []
    probability_of_crossover = random.random()
    if probability_of_crossover < 0.9:
       anak1[:1], anak1[1:] = orangtua1[:1], orangtua2[1:]
       anak2[:1], anak2[1:] = orangtua2[:1], orangtua1[1:]
       anakan.append(anak1)
       anakan.append(anak2)
    else:
        anakan.append(orangtua1)
        anakan.append(orangtua2)
    return anakan

# Mutation and add new individuals to the population
def mutation(anak1, anak2):
    for i in range(len(anak1)):
        probability_of_mutation_for_anak1 = random.randint(0,9)
        if probability_of_mutation_for_anak1 < 0.1:
            anak1[i] = random.randint(0,9)

        probability_of_mutation_for_anak2 = random.randint(0,9)
        if probability_of_mutation_for_anak2 < 0.1:
            anak2[i] = random.randint(0,9)

    return anak1, anak2

# Fungsi elitisme untuk memasukkan kromosom terbaik pada generasi sebelumnya
def elitisme(population, best_kromosom_generation, bad_kromosom, total_fitness):
    if  best_kromosom_generation[1] < bad_kromosom[0] and (best_kromosom_generation[0] not in population):
        population[bad_kromosom[2]] = best_kromosom_generation[0]
        total_fitness = (total_fitness - bad_kromosom[0]) + best_kromosom_generation[1]

        print('\nProses Elitisme')
        print(f'Kromosom Ke-{bad_kromosom[2]+1}: {bad_kromosom[1]}, fitness: {bad_kromosom[0]}')
        print(f'diubah menjadi {best_kromosom_generation[0]}, fitness: {best_kromosom_generation[1]}\n')

    return population, total_fitness

generation = 50
population_total = 20
kromosom_total = 6

population = generate_population(population_total, kromosom_total)
print("Populasi awal:", population)

best_kromosom_generation = []

for genes in range(generation):
   # Inisialisasi variabel untuk proses perhitungan algoritma genetika
      kromosom_data, best_kromosom, bad_kromosom, fitness_data, new_population, child = [], [], [], [], [], []
      total_fitness, count_kromosom, index = 0, 999, 0

      print('\n================================================================')
      print('Generasi', genes+1)
      print('=================================================================')
      # Perulangan untuk mencari nilai phenotype dan nilai fungsi / fitness pada setiap kromosom
      for i, kromosom in enumerate(population):
          kromosom_a, kromosom_b = split_cromosome(kromosom)
          x1 = decode(kromosom_a, x1_batas)
          x2 = decode(kromosom_b, x2_batas)

          fitness_value = function(x1, x2)
          fitness_data.append(fitness_value)
          total_fitness += fitness_value

          # Pencarian Fitness Terkecil Dalam Suatu Generasi
          if genes != 0 and fitness_value < count_kromosom:
                  count_kromosom = fitness_value
                  bad_kromosom = [fitness_value, kromosom, i]


      # Pemilihan Kromosom Dengan Fitness Terbaik
      best_kromosom = best_kromosom_selection(population)

      print("Kromosom Terbaik :", best_kromosom[0])
      print("Fitness Terbaik :", best_kromosom[1])

      # Proses Elitisme untuk memasukkan kromosom terbaik pada generasi sebelumnya
      if genes != 0:
         most_best = sorted(best_kromosom_generation, key=lambda x: x[1], reverse=True)[0]
         population, total_fitness = elitisme(population, most_best, bad_kromosom, total_fitness)

      best_kromosom_generation.append(best_kromosom)

      # Perulangan untuk melakukan seleksi orang tua, crossover dan mutasi anak untuk mendapatkan populasi generasi selanjutnya
      if  genes != generation-1 :
          for i in range(population_total // 2):
              parent_1 = parent_roulette_selection(population, fitness_data, total_fitness)
              parent_2 = parent_roulette_selection(population, fitness_data, total_fitness)
              print(parent_1,parent_2)
              childs = crossover(parent_1, parent_2)
              print(childs)
              child_1, child_2 = mutation(childs[0], childs[1])

              new_population.append(child_1)
              new_population.append(child_2)

          population = new_population

# Memanggil fungsi untuk menentukan kromosom terbaik pada keseluruhan generasi
print('\n=====================================================')
print('Hasil Akhir Kromosom Terbaik')
print('=====================================================')
print('Kromosom Terbaik         = ', most_best[0])
print('Phenotype x              = ', most_best[2])
print('Phenotype y              = ', most_best[3])
print('Nilai Fungsi / Fitness   = ', most_best[1])
print('=====================================================')
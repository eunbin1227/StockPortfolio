# import numpy as np
import random
import csv
import time

def make_initial_chromosomes():
    initial_chromosomes = []
    for i in range(10):
        chromosome = []    
        for j in range(198):
            if random.randint(0, 19) == 19:
                chromosome.append(random.randint(1, 4))
            else:
                chromosome.append(0)
        initial_chromosomes.append(chromosome)
    return initial_chromosomes    


def file_reader():
    result = []
    f = open('../../output/kospi_200.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    for line in rdr:
        result.append(line)
    f.close() 
    return result[1:]


def selection(data):
    data_sum = sum(data)
    point = random.uniform(0, data_sum)
    total = 0
    for i in range(10):
        total += data[i]
        if(point<total):
            return i


def crossover(input1, input2):
    crossover_point = random.randint(1, 196)
    result = input1[:crossover_point] + input2[crossover_point:]
    return result 


def mutation(input, prob):
    for i, value in enumerate(input):
        if value != 0:
            if random.random() < prob:
                input[i] = random.randint(1, 4)

    return input 


def replace(former, fit, replace, k):
    max_value = max(fit)
    max_index = fit.index(max_value)
    max_former = former[max_index]
    del former[max_index]
    indexes = random.sample(range(0, 9), k)
    for i in range(k):
        former[indexes[i]] = replace[i]
    
    return former + [max_former]


def calculate_value(data, chromosome):
    chromosome_sum = sum(chromosome)
    result = 0.0       
    
    for i, value in enumerate(chromosome):
        if chromosome_sum == 0: break
        proportion = value/chromosome_sum
        result += data[i]*proportion
    
    return result

start = time.time()
count_1 = 0
count_2 = 0
f = open('../../output/test6.csv', 'w', encoding='utf-8')
# f.write("\n")
result = []
for num in range(2, 6):
    temp = []
    for i in range(500):
        chromosomes = make_initial_chromosomes()
        stock_data = file_reader()
        fitness_data = [float(i[7]) for i in stock_data]
        yield_data = [float(i[6]) for i in stock_data]
        portfolio_fitnesses = []
        portfolio_yields = []

        #Calculate fitness of chromosomes
        for i in range(10):
            portfolio_fitnesses.append(calculate_value(fitness_data, chromosomes[i]))


        count = 0
        recursion_time = 30

        # Genetic Algorithm
        while True:
            offsprings = []
            k = 3
            for cnt in range(k):
                #Selection
                select_1 = selection(portfolio_fitnesses)
                value = select_1
                while value == select_1:
                    value = selection(portfolio_fitnesses)
                select_2 = value

                #Crossover
                offspring = crossover(chromosomes[select_1], chromosomes[select_2])

                #Mutation
                mutation_prob = float(num/10)
                offspring = mutation(offspring, mutation_prob)

                offsprings.append(offspring)

            chromosomes = replace(chromosomes, portfolio_fitnesses, offsprings, k)
            # print(portfolio_fitnesses)
            # print(sum(portfolio_fitnesses, 0.0)/len(portfolio_fitnesses))
            for i in range(10):
                portfolio_fitnesses[i] = calculate_value(fitness_data, chromosomes[i])
            count += 1
            if count > recursion_time:
                break


        compare_portfolio = make_initial_chromosomes()
        portfolio_yields_compare = []
        for i in range(10):
            portfolio_yields.append(calculate_value(yield_data, chromosomes[i]))
            portfolio_yields_compare.append(calculate_value(yield_data, compare_portfolio[i]))

        best_gen = max(portfolio_yields)
        temp.append(best_gen)
        # avg_gen = sum(portfolio_yields, 0.0)/len(portfolio_yields)
        # avg_comp = sum(portfolio_yields_compare, 0.0)/len(portfolio_yields_compare)
        # f.write("%s,%s\n" %(avg_gen, avg_comp))
        # if avg_gen > avg_comp:
        #     count_1 += 1
        # else:
        #     count_2 += 1
        
        # f.write("%s\n" %(best_gen))
    result.append(temp)

for i in range(50):
    f.write("%s,%s,%s,%s,%s\n"%(i+1, result[0][i], result[1][i], result[2][i], result[3][i]))


# f.write("\n%s,%s\n" %(count_1, count_2))
f.close()
# print(count_1, count_2)
print(time.time() - start)



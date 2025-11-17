import os
import sys
import time
import random
import csv

class Result:

    def __init__(self, solution, duration, c=None):
        self.solution = solution
        self.duration = duration
        self.c = c


class SAT:

    def __init__(self, file_path, file_name: str):
        self.num_variables: int = 0
        self.num_clauses: int = 0
        self.clauses: list[list[int]] = []
        self.file_name = file_name

        self.process_cnf_file(file_path)

    def process_cnf_file(self, file_path: str):

        with open(file_path, 'r') as file:

            line = file.readline()
            while line[0] == 'c':
                line = file.readline()

            if(line != ''):
                metadata = line.split()
                self.num_variables = int(metadata[2])
                self.num_clauses = int(metadata[3])

                # print(f'# Vars: {self.num_variables} | # clauses: {self.num_clauses}')
            else:
                exit("Error processing file.")

            for row in range(self.num_clauses):
                line = file.readline()

                new_clause = line.split()
                new_clause = [ int(new_clause[i]) for i in range(0, len(new_clause) - 1)]
                self.clauses.append(new_clause)

        # print(self.clauses)


    def evaluate_assignment(self, assignment: list[int]):
        result = 0

        for disjunction in self.clauses:

            for literal in disjunction:

                if literal == assignment[abs(literal)]:
                    result += 1
                    break

        return result


    def is_SAT(self, assignment: list[int]):

        for disjunction in self.clauses:

            valid = False

            for literal in disjunction:

                if literal == assignment[abs(literal)]:
                    valid = True
                    break

            if valid == False:
                return False
            
        return True
    

    def get_false_clauses(self, assignment: list[int]):

        result = []

        for disjunction in self.clauses:

            valid = False

            for literal in disjunction:

                if literal == assignment[abs(literal)]:
                    valid = True
                    break

            if valid == False:
                result.append(disjunction)


        return result




    def hill_climb(self, max_iterations):
        start_time = time.process_time()
        
        assignment = [i for i in range(self.num_variables + 1)]
        score = self.evaluate_assignment(assignment)

        iteration = 0

        for iteration in range(max_iterations):

            if self.is_SAT(assignment) == True:
                end_time = time.process_time()
                duration = end_time - start_time
                return Result(assignment, duration, self.evaluate_assignment(assignment))

            # print(f'\nIteration {iteration}')
            # print(f'Starting Assignment: {assignment} | Score: {score}')

            best_assignment = assignment
            best_score = float('-inf')

            for i in range(1, len(assignment)):
                new_assignment = assignment[:]
                new_assignment[i] *= -1

                new_score = self.evaluate_assignment(new_assignment)
                # print(f'New assignment: {new_assignment} | New score: {new_score}')

                if new_score > best_score:
                    best_score = new_score
                    best_assignment = new_assignment
                    # print(f'Best Assignment: {new_assignment} | Score: {new_score}')

            assignment = best_assignment

        end_time = time.process_time()
        duration = end_time - start_time
        return Result('UNSAT', duration, self.evaluate_assignment(assignment))

    
    def walkSAT(self, probability: float, max_flips: int):

        start_time = time.process_time()

        # inital random
        assignment = [i if random.random() < 0.5 else -i for i in range(self.num_variables + 1)]

        
        for iteration in range(max_flips):
            # print(f'\nIteration {iteration}')
            # print(f'Starting Assignment: {assignment} | Score: {self.evaluate_assignment(assignment)}')

            if self.is_SAT(assignment) == True:
                end_time = time.process_time()
                duration = end_time - start_time
                return Result(assignment, duration, self.evaluate_assignment(assignment))
                
            

            false_clauses = self.get_false_clauses(assignment)

            selected_clause = random.choice(false_clauses)
            # print(f'Selected Clause: {selected_clause}')

            if random.random() < probability: 
                
                selected_literal = random.choice(selected_clause)

                assignment[abs(selected_literal)] *= -1

                # print(f'Random Walk: {assignment[abs(selected_literal)]}')

            else:
                best_assignment = []
                best_score = float('-inf')

                for literal in selected_clause:
                    # print(literal)

                    new_assignment = assignment[:]
                    # print(new_assignment)

                    new_assignment[abs(literal)] *= -1

                    new_score = self.evaluate_assignment(new_assignment)

                    # print(f'New assignment: {new_assignment} | New score: {new_score}')

                    if new_score > best_score:
                        best_assignment = new_assignment
                        best_score = new_score
                        # print(f'Best Assignment: {new_assignment} | Score: {new_score}')

                assignment = best_assignment

        end_time = time.process_time()
        duration = end_time - start_time
        return Result('UNSAT', duration, self.evaluate_assignment(assignment))
    

    def early_termination(self, assignment: list[int]):

        for disjunction in self.clauses:

            clause_satisfied = False
            has_none = False

            for literal in disjunction:
                
                current_value = assignment[abs(literal)]

                if current_value is None:
                    has_none = True

                if literal == current_value:
                    clause_satisfied = True
                    break


            if clause_satisfied == False and has_none == False:
                return True
            
        return None
    

    def find_pure_symbols(self, assignment: list[int]):

        false_clauses = self.get_false_clauses(assignment)

        pure_symbols = []
        unpure_symbols = []

        for disjunction in false_clauses:

            for literal in disjunction:

                if literal in unpure_symbols:
                    continue

                if -literal in pure_symbols:
                    pure_symbols.remove(-literal)
                    unpure_symbols.append(-literal)
                    unpure_symbols.append(literal)
                elif literal not in pure_symbols:
                    pure_symbols.append(literal)

        result = []
        for i in pure_symbols:
            if assignment[abs(i)] is None:
                result.append(i)
        
        
        return result
    

    def find_unit_clauses(self, assignment: list[int]):

        false_clauses = self.get_false_clauses(assignment)

        unit_clauses = []

        for disjuction in false_clauses:
            if len(disjuction) == 1:
                unit_clauses.append(disjuction)

        result = []
        for i in unit_clauses:
            if assignment[abs(i[0])] is None:
                result.append(i)
        
        
        return result
    


        


    def DPLL(self):

        start_time = time.process_time()

        assignment = [None for i in range(self.num_variables + 1)]
        print(assignment)

        result = self.recursive_DPLL(assignment)

        end_time = time.process_time()
        duration = end_time - start_time

        if result is None:
            return Result('UNSAT', duration)

        return Result(result, duration)


    def recursive_DPLL(self, assignment):
        # print(assignment)

        if self.is_SAT(assignment) == True:
            return assignment
        
        if self.early_termination(assignment) == True:
            return None
        
        pure_symbols = self.find_pure_symbols(assignment)
        # print(f'Pure_symbols: {pure_symbols}')

        if(len(pure_symbols) > 0):
            new_assignment = assignment[:]
            # new_assignment[abs(pure_symbols[0])] = pure_symbols[0]
        
            for i in pure_symbols:
                new_assignment[abs(i)] = i

            return self.recursive_DPLL(new_assignment)
        
        unit_clauses = self.find_unit_clauses(assignment)
        # print(f'Unit Clauses: {unit_clauses}')

        if(len(unit_clauses) > 0):
            new_assignment = assignment[:]
            # new_assignment[abs(unit_clauses[0])] = unit_clauses[0]

            for i in unit_clauses:
                new_assignment[abs(i)] = i

            return self.recursive_DPLL(new_assignment)
        

        unassigned_indexes = []

        for i in range(1, len(assignment)):
            if assignment[i] is None:
                unassigned_indexes.append(i)

        if len(unassigned_indexes) == 0:
            return None
        
        new_assignment_true = assignment[:]
        new_assignment_true[unassigned_indexes[0]] = unassigned_indexes[0]

        new_assignment_false = assignment[:]
        new_assignment_false[unassigned_indexes[0]] = -unassigned_indexes[0]

        return self.recursive_DPLL(new_assignment_true) or self.recursive_DPLL(new_assignment_false)


def run_walksat_experiment():

    # directory = 'A3_tests/'
    directory = 'A3Formulas/'

    log_file_path = 'results/walksat_log.csv'
    result_file_path = 'results/walksat_results.csv'

    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)

        durations = []
        clause_satisfied = []

        for _ in range(10):
            axo = SAT(file_path, file_name)
            result = axo.walkSAT(0.5, 100000)

            durations.append(result.duration)
            clause_satisfied.append(result.c)

            print(f'File: {file_name} | SAT: {result.solution} | Time: {result.duration} | C: {result.c}')

            with open(log_file_path, 'a') as file:
                writer = csv.writer(file)
                writer.writerow([file_name, result.solution, result.duration, result.c])

        with open(result_file_path, 'a') as file:
            writer = csv.writer(file)
            avg_duration = sum(durations) / len(durations)
            avg_clause_satisfied = sum(clause_satisfied) / len(clause_satisfied)
            writer.writerow([file_name, avg_duration, avg_clause_satisfied])
        

def run_hillclimb_experiment():

    # directory = 'A3_tests/'
    directory = 'A3Formulas/'

    log_file_path = 'results/hillclimb_log.csv'
    result_file_path = 'results/hillclimb_results.csv'

    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)

        axo = SAT(file_path, file_name)
        result = axo.hill_climb(100000)

        print(f'File: {file_name} | SAT: {result.solution} | Time: {result.duration} | C: {result.c}')

        with open(log_file_path, 'a') as file:
            writer = csv.writer(file)
            writer.writerow([file_name, result.solution, result.duration, result.c])


def run_DPLL_experiment():

    # directory = 'A3_tests/'
    directory = 'A3Formulas/'

    log_file_path = 'results/dpll_log.csv'
    result_file_path = 'results/dpll_results.csv'

    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)

        axo = SAT(file_path, file_name)
        result = axo.DPLL()

        print(f'File: {file_name} | SAT: {result.solution} | Time: {result.duration}')

        with open(log_file_path, 'a') as file:
            writer = csv.writer(file)
            writer.writerow([file_name, result.solution, result.duration])

def main():
    # run_walksat_experiment()
    # run_hillclimb_experiment()
    run_DPLL_experiment()


if __name__ ==  '__main__':
    main()
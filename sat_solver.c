#include <stdio.h>
#include <stdlib.h>

void read_cnf_file(FILE *input_file,int **clauses, int *clause_sizes){

    int clause_index = 0;
    char buffer[256];

    while (fgets(buffer, sizeof(buffer), input_file) != NULL)
    {
        if (buffer[0] == 'p'){ continue; }
        
        int literal;
        int num_literals = 0;
        
        //start of str
        char *temp = buffer;

        while (sscanf(temp, "%d", &literal) == 1)
        {
            if (literal == 0){ break; }
            
            num_literals++;
            printf("Found: %d\n", literal);

            while (*temp != ' ' && *temp != '\0') {
                temp++;
            }
            if (*temp != '\0') {
                temp++;
            }
        }

        //only if we actually found literals
        if (num_literals > 0) {
            printf("Literals Found: %d\n", num_literals);

            //malloc mem
            clauses[clause_index] = malloc(sizeof(int) * num_literals);
            
            temp = buffer;
            int literal_index = 0;

            while (sscanf(temp, "%d", &literal) == 1) {
                if (literal == 0){ break; }

                clauses[clause_index][literal_index] = literal;
                literal_index++;
                while (*temp != ' ' && *temp != '\0') {
                    temp++;
                }
                if (*temp != '\0') {
                    temp++;  // Skip the space
                }
            }

            clause_sizes[clause_index] = num_literals;
            clause_index++;
        }

    }
}

void print_clauses(int **clauses, int *clause_sizes){
    // Print the clauses (just to verify)
    for (int i = 0; i < sizeof(clauses); i++) {
        printf("Clause %d: ", i);
        for (int j = 0; j < clause_sizes[i]; j++) {
            printf("%d ", clauses[i][j]);
        }
        printf("\n");
    }
}


int main(int argc, char *argv[]) {

    if (argc != 2) {
        fprintf(stderr, "Usage: %s <filename>\n", argv[0]);
        return EXIT_FAILURE;
    }

    FILE *input_file = fopen(argv[1], "r");
    if (input_file == NULL) {
        printf("Error in opening file");
        return 1;
    }

    int num_variables;
    int num_clauses;
    fscanf(input_file, "p cnf %d %d", &num_variables, &num_clauses);

    printf("# of Variables: %d | # of Clauses: %d\n", num_variables, num_clauses);

    int **clauses = malloc(sizeof(int *) * num_clauses);
    int *clause_sizes = malloc(sizeof(int) * num_clauses);  // Array to store the size of each clause

    read_cnf_file(input_file, clauses, clause_sizes);
    
    print_clauses(clauses, clause_sizes);



    // int *varibles = malloc();
    

    // Free memory
    for (int i = 0; i < num_clauses; i++) {
        free(clauses[i]);
    }
    free(clauses);
    free(clause_sizes);

    fclose(input_file);
    return 0;
}

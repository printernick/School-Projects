#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#define MAX 256

int main(int argc, char* argv[])
{
	char* environmentVariable = getenv("EVERY");
	int N = 1;
	int M = 1;
	bool hasOption = false;

	//no additional arguments
	if (argc == 1)
	{
		if (environmentVariable)
		{
			sscanf(environmentVariable, "-%d, %d", &N, &M);
		}

	}
	else
	{
		
		//check if first argument is an option
		if (strncmp(argv[1], "-", 1) == 0)
		{
			//parse option and set values
			sscanf(argv[1], "-%d, %d", &N, &M);
			hasOption = true;
		}
		else
		{
			if (environmentVariable)
			{
				sscanf(environmentVariable, "-%d, %d", &N, &M);
			}

		}

	}
	
	//check valid N and M
	
	if (N <= 0 || M < 0 || M > N)
	{
		printf("%s\n", "invalid value for N or M");
		return -1;
	}

	char buf[MAX];
	int counterN;
	int counterM;

	//for for loops
	int i;

	//no file arguments passed, so read from stdin
	if (argc == 1 || (argc == 2 && hasOption))
	{
		counterN = 0;
		counterM = M;
		//READ FROM STDIN
		while (fgets(buf, MAX, stdin) != NULL)
		{
			
			if (counterN % N == 0)
			{
				counterN = 0;
				counterM = M;
			}
			if (counterM > 0)
			{
				printf("%s", buf);
				counterM--;
			}
			counterN++;
		}
		return 0;
	}
	//start at one after 
	else if (hasOption)
	{
		i = 2;
	}
	else
	{
		i = 1;
	}

	for (i; i < argc; i++)
	{
		FILE* file = fopen(argv[i], "r");
		if (file)
		{
			counterN = 0;
			counterM = M;
			while (fgets(buf, MAX, file) != NULL)
			{
			
				if (counterN % N == 0)
				{
					counterN = 0;
					counterM = M;
				}
				if (counterM > 0)
				{
					printf("%s", buf);
					counterM--;
				}
				counterN++;
			}
			
		}
	}


	return 0;
}

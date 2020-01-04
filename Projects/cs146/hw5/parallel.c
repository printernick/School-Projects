#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <sys/sysinfo.h>
#include <sys/wait.h>


int main(int argc, char* argv[])
{

	int opt;
	int shellIndex = 0;
	while((opt = getopt(argc, argv, "s:")) != -1)
	{
		switch(opt)
		{
			case 's':
				shellIndex = optind-1;
				break;
		}
	}

	
	unsigned int N;
	char* shell; 

	//Set shell
	if (shellIndex == 0)
	{
		shell = getenv("SHELL");
	}
	else
	{
		shell = argv[shellIndex];
	}

	//Set N
	if (argc == 2 && shellIndex == 0)
	{
		N = atoi(argv[1]);
	}
	else if (argc == 4)
	{
		N = atoi(argv[3]);
	}
	else
	{
		N = get_nprocs();
	}


	pid_t parentPid = getpid();
	unsigned int numOfRunningProcesses = 0;
	unsigned int failedChildren = 0;

	char command[BUFSIZ];
	while (fgets(command, sizeof command, stdin) != NULL)
	{
		char* args[3];
		args[0] = shell;
		args[1] = "-c";
		args[2] = command;
		
		if (numOfRunningProcesses <= N)
		{
			if (parentPid == getpid())
			{
				numOfRunningProcesses++;
				if (fork() == 0)
				{
					execv(shell, args);
				}

				if (numOfRunningProcesses == N)
				{
					if (wait(0) != -1)
					{
						numOfRunningProcesses--;
					}
					else
					{
						failedChildren++;
					}
				}
			}
		}
	}

	//Reap leftover processes
	while (wait(0) != -1)
	{
		wait(0);
	}

	return failedChildren;
}


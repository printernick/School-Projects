#include <stdio.h>
#include <sys/stat.h>
#include <limits.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char* argv[])
{
	if (argc == 1)
	{
		printf("%s\n", "unrm: missing operand");
		return -1;
	}
	
	char trashPath[PATH_MAX] = "/tmp/.trash/";
	mkdir(trashPath, 0777);

	int i;
	for (i = 1; i < argc; i++)
	{		
		//move the file
		char fullPath[PATH_MAX];
		realpath(argv[i], fullPath);
				
		char newPath[PATH_MAX];
		strcpy(newPath, trashPath);
		strcat(newPath, argv[i]);

		if (rename(newPath, fullPath))
		{
			printf("%s does not exist or already exists\n", argv[i]);
		}
			
	}
	
	return 0;

}

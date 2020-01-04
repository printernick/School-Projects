#include <stdio.h>
#include <sys/stat.h>
#include <stdlib.h>
#include <limits.h>
#include <string.h>
#include <dirent.h>
#include <unistd.h>


void emptyDir(char currentPath[PATH_MAX])
{
	DIR* dirp = opendir(currentPath);
	struct dirent* file;
	if (dirp != NULL)
	{
		while ((file = readdir(dirp)) != NULL)
		{
			if (strcmp(file->d_name, ".") != 0 && strcmp(file->d_name, "..") != 0)
			{
				char newPath[PATH_MAX];
				strcpy(newPath, currentPath);
				strcat(newPath, file->d_name);
		
				if (opendir(newPath))
				{
					char withSlash[PATH_MAX];
					strcpy(withSlash, newPath);
					strcat(withSlash, "/");

					emptyDir(withSlash);
					rmdir(newPath);
				}
				else
				{
					remove(newPath);
				}
			}
		}
		closedir(dirp);
	}
}

int main(int argc, char* argv[])
{
	if (argc != 1)
	{
		printf("%s\n", "trash: takes no arguments");
	}

	char trashPath[PATH_MAX] = "/tmp/.trash/";
	mkdir(trashPath, 0777);

	emptyDir(trashPath);
	

	return 0;
}

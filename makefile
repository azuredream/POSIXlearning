main : main.o
	cc -o main main.o
main.o :  src/main.c includes/errors.h
	cc -c -g src/main.c
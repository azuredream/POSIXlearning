objs = main.o
VPATH = src:includes

main : $(objs)
	cc -o main $(objs)
main.o :  errors.h tprint.h
.PHONY : clean
clean :
	rm main $(objs)
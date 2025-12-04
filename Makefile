

all : dp_prog

dp_prog : dp.cpp
	g++ -o dp_prog -Wall dp.cpp
make clean :
	rm -f dp_prog
// based on GCD.cpp
// adapted by folkert@vanheusden.com
// further by torsten.knoefel@gmail.com
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include "QPULib.h"

#ifdef DEBUG 
#define D(x) (x)
#else 
#define D(x) do{}while(0)
#endif

void gcd(Ptr<Int> p, Ptr<Int> q, Ptr<Int> r)
{
  Int a = *p;
  Int b = *q;
  While (any(a != b))
    Where (a > b)
      a = a-b;
    End
    Where (a < b)
      b = b-a;
    End
  End
  *r = a;
}

int get_temp()
{
	FILE *fh = fopen("/sys/devices/virtual/thermal/thermal_zone0/temp", "r");

	char buf[128];
	fgets(buf, sizeof buf, fh);

	fclose(fh);

	return atoi(buf);
}

int main(int argc, char *arv[])
{

	// Construct kernel
	auto k = compile(gcd);

	k.setNumQPUs(12);

	// Allocate and initialise arrays shared between ARM and GPU
//#define N 512   // was 4096
//#define N 6000   // was 4096
#define N 600 //6000
#define M 600000
	SharedArray<int> a(M), b(M);

	SharedArray<int> r(M);

	// Invoke the kernel and display the result
//	for(int j = 0; j < 20000; j++) {
	int t,d;
	for(;;) {
		t = get_temp();
		d = abs(73000-t) / 10;
D(printf("%d  %d", d, N*d));
//		printf("%d", t);
		d = N*d;
		if (d > M)
			d = M;
		if (t < 70000) {
			for (int i = 0; i < d; i++) {
				a[i] = 97;
				b[i] = 89;
			}
			k(&a, &b, &r);
			D(printf("%s"," ******\n"));
		}
		else {
			usleep(2000); //was 101000 //5000
			D(printf("%s","\n"));
		}
	}

	return 0;
}

//

# include <stdio.h>

	int main() {
	
	int a, b, c, d;
	
	printf("Please enter 4 numbers separated by spaces > ");
	scanf("%d%d%d%d", &a, &b, &c, &d);
	
	if(a < b && a < c && a < d)
    	printf( "%d is the smallest number\n", a);
 
    	else if(b < a && b < c && b < d)
    	printf( "%d is the smallest number\n", b);
 
    	else if(c < a && c < b && c < d)
    	printf( "%d is the smallest number\n", c);
 
    	else if(d < a && d < b && d < c )
    	printf( "%d is the smallest number\n", d);
 
	return 0;
	
	}
	
		
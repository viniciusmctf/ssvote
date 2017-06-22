from math import *
from random import randint

# This function determines the multiplicative inverse of a number n,
# in a finite field of size field
def mult_inverse(n, field):
	(t, next_t) = (0, 1)
	(r, next_r) = (field, n)
	while next_r != 0:
		q = r // next_r
		(t, next_t) = (next_t, t - q*next_t)
		(r, next_r) = (next_r, r - q*next_r)
	if (r > 1):
		print("You can't inverse \'n\' in this field\n")
		return 0
	if t < 0:
		t = t + field
	return t

# This function defines a Polynomial in a determined field "prime"
def f(x, coefs, prime):
	y = 0
	count = 0
	for i in coefs:
		y = (y + i*pow(x,count)) % prime
		count += 1
	return y

# This function creates the shamir shares
# Text book share creation. Algorithm in the report
def create_shares(n, k, secret, prime):
	assert(secret < prime), ("The secret must be smaller than the field\n")
	coef_list = []
	coef_list.append(secret)
	for i in range(k-1):
		coef_list.append(randint(0, prime))
	points_list_x = []
	points_list_y = []
	count = 1
	for i in range(n):
		points_list_x.append(count)
		points_list_y.append(f(count, coef_list, prime))
		count += 1
	shares = []
	for i in range(n):
		shares.append((points_list_x[i], points_list_y[i]))
	return shares

# This function rebuilds the secret using polynomial interpolation
# in a finite field
def reconstruct_secret(list_of_shares, k, prime):
	assert(len(list_of_shares) >= k), ("Not enough shares.\n")
	secret = 0
	for (x, y) in list_of_shares:
		temp = 1
		for (xi, _) in list_of_shares:
			if xi == x: 
				continue
			diff = (xi - x) % prime
			temp = (temp * xi * mult_inverse(diff, prime)) % prime
		secret = (secret + y * temp) % prime
	return secret

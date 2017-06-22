from ssss import *

#This function creates a poll based on a question, 
#   2 options, a number of expected votes, a prime modulus, 
#   a minimum number of votes and a shared password
def create_poll(question, options, n_votes, prime, threshold, secret):
	assert(n_votes > 1), ("You need at least 2 expected votes")
	assert(len(options) == 2), ("You need 2 voting options, %i" % len(options))
	print(question)
	print("Options: 1. "+options[0]+"; 2. "+options[1])
	votes = []
	return [votes, create_shares(n_votes, threshold, secret, prime)]

#Global variables for this tests
question = "Testing poll, does it work?"
options = ["Yes", "No"]
n_votes = 10
prime = 367
threshold = 6
secret = 42
vote_count = 0
vote_type_one = 0
[votes, shares] = [[],[]]

if __name__ == "__main__":

	#This function agregates votes on a list
	def vote(this_option):
		global vote_count
		global vote_type_one
		global shares
		global options
		if this_option == options[0]:
			vote_type_one = vote_type_one + 1
		votes.append(shares[vote_count])
		vote_count = vote_count + 1

	#This function prints the results of a voting
	def print_result():
		global vote_count
		global vote_type_one
		global options
		print("Poll result:")
		print("1. "+options[0]+": "+str(vote_type_one))
		print("2. "+options[1]+": "+str(vote_count-vote_type_one))


	#The following tests are meant to test if the voting system
	# works and if it is safe, so no outsider can put a vote in
	print("TESTING WITH K VOTES")
	
	# Poll created with the original shares used to make 
	# a legit vote
	[votes, shares] = create_poll(question, options, n_votes, prime, threshold, secret)
	
	# Each of up to //threshold// voters contribute with
	# their votes
	for i in range(threshold):
		vote(options[randint(0,1)])

	if (vote_count > threshold):
		# The secret is reconstructed to verify if votes are
		# legit
		test = reconstruct_secret(votes, threshold, prime)
		assert(test == secret), ("Test 1 FAILED, impossible to reconstruct secret with K votes")

	print_result()
	print("TEST WITH K VOTES OK")
	vote_count = 0
	vote_type_one = 0
	
	# In this test the maximum number of voters //n_votes// is used
	print("TESTING WITH N VOTES")
	[votes, shares] = create_poll(question, options, n_votes, prime, threshold, secret)
	for i in range(n_votes):
		vote(options[randint(0,1)])

	if (vote_count > threshold):
		test = reconstruct_secret(votes, threshold, prime)
		assert(test == secret), ("Test 2 FAILED, impossible to reconstruct secret with N votes")
	print_result()
	print("TEST WITH N VOTES OK")
	
	# In this test, all voters are fake
	print("TESTING WITH ONLY FAKE VOTES")
	vote_count = 0
	vote_type_one = 0
	[votes, shares] = create_poll(question, options, n_votes, prime, threshold, secret)
	for i in range(n_votes):
		votes.append((i, randint(0, prime)))
		vote_count = vote_count + 1
		vote_type_one = vote_type_one + 1

	if (vote_count > threshold):
		test = reconstruct_secret(votes, threshold, prime)
		assert(test != secret), ("Test 3 FAILED, fake votes verified as true")
		print("Received: "+str(test)+", expected: "+str(secret)+". Voting failed")
	print_result()
	print("ALL FAKE TEST OK")
	
	# In this test, all but one voters are legit
	print("TESTING WITH ONE FAKE VOTE")
	vote_count = 0
	vote_type_one = 0
	[votes, shares] = create_poll(question, options, n_votes, prime, threshold, secret)
	for i in range(threshold):
		vote(options[randint(0,1)])
	votes.append((i, randint(0, prime)))
	vote_count = vote_count + 1
	vote_type_one = vote_type_one + 1

	if (vote_count > threshold):
		test = reconstruct_secret(votes, threshold, prime)
		assert(test != secret), ("Test 3 FAILED, fake votes verified as true")
		print("Received: "+str(test)+", expected: "+str(secret)+". Voting failed")
	print_result()
	print("ONE FAKE TEST OK")
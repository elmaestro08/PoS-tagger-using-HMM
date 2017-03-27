File hmmlearn.py learns a hidden Markov model from the training data, and hmmdecode.py uses the model to tag new data.

python hmmlearn.py /path/to/input

The argument is a single file containing the training data; the program learns a hidden Markov model, and writes the model parameters to a file called hmmmodel.txt. 

The tagging program will be invoked in the following way:

python hmmdecode.py /path/to/input

The argument is a single file containing the test data; the program reads the parameters of a hidden Markov model from the file hmmmodel.txt, tags each word in the test data, and writes the results to a text file called hmmoutput.txt in the same format as the training data.

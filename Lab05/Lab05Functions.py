'''
Author: Reid Dye

Here's my code to generate all of the pretty graphs for Lab05!
To make this run correctly, make sure the data is in the same folder as this file.
'''

# import alllllll the libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re #fml
from collections import Counter
from os import path

# read the data
df = pd.read_csv(
    re.sub(
        '[^/]+(\.py)|(\.pyc)$',  #matches the last part of the path to this file (i.e. /Users/Reidddye/.../ATCS/Lab05/Lab05.py)
        '', # just delete that stuff, we don't need it                                                               ^^^^^^^^^
        path.realpath(__file__) # the full path to this file (the string we're looking through)
    )+'Lab05Data.tsv', #add on the dataset's filename in place of this file
    sep='\t' #set separator as tabs instead of commas (csv -> tsv)
)

# define our hash functions, and make them work on vectors/df columns
def unicode_hash(key, buckets=np.Inf): 
    return int(sum(
        map(ord, key)
    )%buckets)
def python_hash(key, buckets=np.Inf):
    return hash(key) if buckets == np.Inf else int(hash(key)%buckets)

python_hash  = np.vectorize(python_hash,  excluded={'buckets'})
unicode_hash = np.vectorize(unicode_hash, excluded={'buckets'})

# function to find collisions with my name
def get_collisions(df, hash_fn, name='Dye, Reid', buckets=100):
    return df[
        hash_fn(df['Student Name'], buckets=buckets) == 
        hash_fn(name,               buckets=buckets)
    ]

# function to count the total number of collisions
def count_collisions(df, hash_fn, buckets):
    return len(df)- len(
                    Counter(
                    hash_fn(
                        df['Student Name'], 
                        buckets=buckets
                    )))

# plot the histograms
def histograms():
    fig, ax = plt.subplots(1, 2, sharex=True, sharey=True)
    ax[0].hist(unicode_hash(df['Student Name'], buckets=100))
    ax[1].hist(python_hash(df['Student Name'], buckets=100))
    ax[0].set_xlabel('Hash')
    ax[1].set_xlabel('Hash')
    ax[0].set_ylabel('Frequency')
    ax[0].set_title('Unicode Hash')
    ax[1].set_title('Python Hash')

    fig.suptitle('Distribution of Hashes for Different Hash Functions')
    plt.show()

# plot the collisions vs buckets graphs
def buckets_graph():
    x = [2**i for i in range(5, 20)]
    y1 = [count_collisions(df, unicode_hash, 2**i) for i in range(5, 20)]
    y2 = [count_collisions(df, python_hash, 2**i) for i in range(5, 20)] 

    plt.plot(x, y1, label='Unicode Hash')
    plt.plot(x, y2, label='Python Hash')
    plt.xscale('log')
    plt.legend()
    plt.xlabel('Buckets')
    plt.ylabel('Collisions')
    plt.title('Collisions vs. Number of Buckets of Python Hash and Unicode Hash')

    plt.show()

if __name__ == '__main__':
    print('unicode hash conflicts:', len(get_collisions(df, unicode_hash)))
    print('python hash conflicts:', len(get_collisions(df, python_hash)))

    # print it all out in a pretty way, to make copying into a markdown table easy
    print()
    print(
        '| row' #add this on because it is not included in the pd.df -> plaintext conversion

        + re.sub(
            '[ \t]{2,}', ' | ',                             # match length 2+ whitespace and replace with ' | ' for the md table
            get_collisions(df, unicode_hash)                # get the collisions (returns pd.df)
                .to_string()                                # convert to plaintext
                .replace('\n', '  \n  ')                    # replace the ends of lines with things with extra spaces so we get | at the start and end of each row/line
                .replace('\n', '\n| -- | -- | -- |\n', 1)   # insert the header vs data splitter thing after the first newline
        ) 

        + ' |' # add a final pipe, which we were missing before since the last line does not include a newline
    )
    print()
    # same as above but just as written, not expanded to look pretty
    print('| row' + re.sub('[ \t]{2,}', ' | ', get_collisions(df, python_hash).to_string().replace('\n', '  \n  ').replace('\n', '\n| -- | -- | -- |\n', 1)) + ' |')

    
    # graphs
    histograms()
    buckets_graph()
    

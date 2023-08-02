# Use the Cinemagoer API to find a path to different movies
# James Natoli, 2023
# NB: "Since the end of 2017, IMDb has removed the Character kind of information. "

# This incredible api
from imdb import Cinemagoer

# My Linked List class
import MovieChain

import argparse
parser = argparse.ArgumentParser( description='Find movies to watch')
parser.add_argument( '-f', '--from', dest='fromMovie', action="store", default='Fargo', required=False,
                     help='The movie you are starting at', type=str)
parser.add_argument( '-t', '--to',   dest='toMovie', action="store", default='The Big Lebowski', required=False,
                     help='The movie you are trying to reach', type=str)
parser.add_argument( '-c', '--confirm', dest='confirmMovie', action="store_true", default=False, required=False,
                     help='Confirm selection of the correct movies')

def selectMovie( search, confirmMovie=True):
    """Helper function to select a movie"""
    flagship = Cinemagoer()
    for mv in flagship.search_movie( search):
        if mv["kind"] != "movie":
            continue
        print( f'Title: {mv["title"]}')
        print( f'Year:  {mv["year"]}')
        # add starring here... top 3 prolly good enough?
        if not confirmMovie or (input("Is this the movie you want? (yes/no)\n").lower() == "yes"):
            return flagship.get_movie( mv.movieID)

    print("Couldn't find the movie that you wanted :(")
    print("Exiting...")
    exit(1)

def selectMovies( args):
    return ( selectMovie( args.fromMovie, args.confirmMovie), selectMovie( args.toMovie, args.confirmMovie))

def movieOverlap( movie1, movie2, lim=10):
    """Determine if 2 movies have any of the same actors*"""
    return (set(movie1['cast'][0:lim]).intersection( movie2['cast'][0:lim]), set(movie2['cast'][0:lim]).intersection( movie1['cast'][0:lim]))
    
def expandedMovieOverlap( movie1, movie2):
    """Determine if 2 movies have any of the same actors*"""
    return (set(movie1['cast']).intersection( movie2['cast']), set(movie2['cast']).intersection( movie1['cast']))

# Ok, so it works! Now i just need a way to save these combinations and iterate through them?
# because it can potentially be quite complicated...
def main():
    args = parser.parse_args()
    flagship = Cinemagoer()
    movie1, movie2 = selectMovies( args)
    print("Now we have our movies!\n")

    overlapFrom, overlapTo = movieOverlap( movie1, movie2)
    if (len(overlapFrom) == 0):
        print( "No common actors among the first 10... expanding search to all")
        overlapFrom, overlapTo = expandedMovieOverlap( movie1, movie2)
        
    if (len(overlapFrom) == 0):
        print( "No common actors, checking for first order connections")

    i = 0
    castMovie1 = movie1['cast']
    while len(overlapFrom) == 0:
        # I wonder if I could put this in parallel to speed things up...
        print( f'Checking movies with {castMovie1[i]}')
        adjascentMovies = flagship.get_person( castMovie1[i].personID)['filmography']['actor']
        j = 0
        while len(overlapFrom) == 0:
            print( f'Checking {adjascentMovies[j]}...')
            if adjascentMovies[j] is movie1: # skip the same movie...
                continue
            overlapFrom, overlapTo = expandedMovieOverlap( flagship.get_movie( adjascentMovies[j].movieID), movie2)
            j = j + 1
        # print( f'Nothing found for {castMovie1[i]}, moving on to next actor')
        i = i + 1
        
    for (actor1, actor2) in zip( overlapFrom, overlapTo):
        print( f'{actor1} played {actor2.currentRole} in {movie1["title"]} and {actor1.currentRole} in {movie2["title"]}')

    # print("\nShe was also in...")
    # for mv in flagship.get_person( flagship.search_person( actor1['name'])[0].personID)['filmography']['actress'][0:7]:
    #     if (mv["title"] is not movie1["title"]) or (mv["title"] is not movie2["title"]):
    #         print(f'{mv["title"]}')
    # if (len(overlapFrom) == 0):
    #     print( "No common actors among the first 10... expanding search to all")
    #     overlapFrom, overlapTo = expandedMovieOverlap( movie1, movie2)
    # 
    # if (len(overlapFrom) == 0):
    #     print( "No common actors")
    # else:
    #     for (actor1, actor2) in zip( overlapFrom, overlapTo):
    #         print( f'{actor1} played {actor1.currentRole} in {movie1["title"]} and {actor2.currentRole} in {movie2["title"]}')

    print("\nDone :)")
    
if __name__ == "__main__":
    main()
    
    # I can't get director to work :(
    # flagship.update( movie1, info=['director'])
    # for director in movie1['directors']:
    #     print( director['name'])

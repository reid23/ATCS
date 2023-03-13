# quick class to hold a question and an answer or subsequent question
class Node:
    def __init__(self, question, next_if_true, next_if_false):
        """init a Node with a question, and subsequent questions or guesses

        Args:
            question (str): the question represented by this Node
            next_if_true (str, Node): str if next thing is a guess, Node if next thing is another question
            next_if_false (str, Node): str if next thing is a guess, Node if next thing is another question
        """
        self.q = question
        self.t = next_if_true
        self.f = next_if_false

    # define getters and setters for the true and false branches
    @property
    def true(self): return self.t
    @property
    def false(self): return self.f
    @true.setter
    def set_true(self, val): self.t = val
    @false.setter
    def set_false(self, val): self.f = val

    # for debugging, isn't actually used
    # will print out the entire tree using this node as the root
    def __repr__(self):
        return f'Node({self.q}, {self.t}, {self.f})'
    
    
# actual class that holds the tree and does stuff with it
# after writing this, I realized that there's only one
# variable and one method; it didn't need to be a class at all.
# but I already wrote it so lol we're going with it
class DecisionTree:
    def __init__(self):
        """init a decision tree with the base question
        """
        self.qs = Node('Is it bigger than a bread box?', 'Elephant', 'Mouse')
    def ask(self):
        """play one game of twenty questions
        """
        # cur var which will be our focus node 
        # as we make our way down the tree
        cur = self.qs
        # previous node, so once we get to a leaf 
        # we can backtrack one node to add additional questions
        prev = None 
        # tracks which leaf of the previous 
        # node we should add questions to
        prev_answer = None

        # main loop
        # runs 20 times for 20 questions
        for _ in range(20):
            match cur:
                # if cur is a node, it means we have to ask another question
                case Node(q = question):
                    # ask the question and do input validation
                    while not (ans := input(f'{question} [y/n]: ').lower()) in ['y', 'n']:
                        print(f"Invalid answer! Expected 'y' or 'n' but received {ans}.")
                    
                    # update prev before we move the cur pointer
                    prev = cur

                    # move cur down to the correct subtree and update prev_answer accordingly
                    # prev_answer represents the answer the player just gave
                    match ans:
                        case 'y': 
                            cur = cur.true
                            prev_answer =  True
                        case 'n': 
                            cur = cur.false
                            prev_answer = False

                    # now we will go back and loop again!
                
                # if cur is a string we don't have any more questions and we must guess.
                case str(guess):

                    # make the guess and get input, doing input validation
                    while not (ans := input(f'Is it a(n) {guess}? [y/n]: ').lower()) in ['y', 'n']:
                        print(f"Invalid answer! Expected 'y' or 'n' but received {ans}.")

                    # if we got it right, just say yay and return - the game is over
                    if ans == 'y':
                        print('Yay, I guessed it!\n')
                        return
                    
                    # now we know we got it wrong :(
                    # get the correct answer
                    answer = input("Oh no, I couldn't get it!\nWhat were you thinking of? ")

                    # and get a new question to distinguish that answer
                    new_question = input(f"What is a yes/no question that distinguishes it from {guess}? ")
                    while not (new_answer := input(f"Is yes or no the correct answer to get to {answer}? [y/n]: ").lower()) in ['y', 'n']:
                        print(f"Invalid answer! Expected 'y' or 'n' but received {new_answer}.")
                    
                    # now we go back up to the previous node and replace the leaf
                    # we went down (which was just a guess) with a new Node object. 
                    # The new Node asks the new question to distinguish between our 
                    # original answer and the new one.
                    if prev_answer:
                        prev.true = Node(new_question, *((answer, guess) if new_answer=='y' else (guess, answer)))
                    else:
                        prev.false = Node(new_question, *((answer, guess) if new_answer=='y' else (guess, answer)))
                    
                    # print goodbye message and return bc the game's over
                    print('Got it-- Thanks!\n')
                    return
        # if we got past the for loop, we ran out of questions, so the game is over and we lost but we don't get to add a question.
        print("Oh no! I couldn't get it in twenty questions. You win!")

# code to actually run the game
if __name__ == "__main__":
    # init the decision tree object
    dt = DecisionTree()
    
    # introduction message
    print("Welcome to Twenty Questions\nThink of something and I'll try to guess it asking at most 20 questions.\n")

    # main game loop
    while True:
        # play a game
        dt.ask()

        # ask to play again, with input validation
        while not (play_again := input("Do you want to play again? [y/n]: ").lower()) in ['y', 'n']:
            print(f"Invalid answer! Expected 'y' or 'n' but received {play_again}.")
        
        # if they don't want to play again, exit the while loop
        if play_again == 'n': break

    # goodbye message
    print('Thanks for playing!')






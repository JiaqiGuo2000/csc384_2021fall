# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        foods = newFood.asList()
        for ghost_index in range(len(newGhostStates)):
            ghost = successorGameState.getGhostPosition(ghost_index + 1)
            if manhattanDistance(newPos, ghost) <= 1:
                # make sure the pacman is away from ghosts by giving a minimal score to such cases
                return -9999999

        if len(foods) == 0:
            return 0
            # no food left means winning, and we always go for win!

        score = -9999999

        for food_index in range(len(foods)):
            curr_score = - manhattanDistance(foods[food_index], newPos) - 1000 * len(foods)
            # encourage the pacman to get more food by penalizing the score with more food left
            if curr_score > score:
                score = curr_score

        return score

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def _DFMiniMax(curr_game_state, curr_depth):
            best_move = None
            if curr_depth >= self.depth * curr_game_state.getNumAgents():
                return best_move, self.evaluationFunction(curr_game_state)

            if curr_game_state.isWin() or curr_game_state.isLose():
                return best_move, self.evaluationFunction(curr_game_state)  # terminal state!

            if curr_depth % curr_game_state.getNumAgents() == 0:  # player(pos) == MAX
                value = -99999999  # value = -infinity
            else:  # player(pos) == MIN
                value = 99999999  # value = infinity

            for action in curr_game_state.getLegalActions(curr_depth % curr_game_state.getNumAgents()):
                next_state = curr_game_state.generateSuccessor(curr_depth % curr_game_state.getNumAgents(), action)
                next_move, next_value = _DFMiniMax(next_state, curr_depth+1)  # recursive call
                if curr_depth % curr_game_state.getNumAgents() == 0 and value < next_value:
                    value, best_move = next_value, action
                if curr_depth % curr_game_state.getNumAgents() != 0 and value > next_value:
                    value, best_move = next_value, action

            return best_move, value

        return _DFMiniMax(gameState, 0)[0]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def _AlphaBeta(curr_game_state, alpha, beta, curr_depth):
            best_move = None
            if curr_depth >= self.depth * curr_game_state.getNumAgents():
                return best_move, self.evaluationFunction(curr_game_state)

            if curr_game_state.isWin() or curr_game_state.isLose():
                return best_move, self.evaluationFunction(curr_game_state)  # terminal state!

            if curr_depth % curr_game_state.getNumAgents() == 0:  # player(pos) == MAX
                value = -99999999  # value = -infinity
            else:  # player(pos) == MIN
                value = 99999999  # value = infinity

            for action in curr_game_state.getLegalActions(curr_depth % curr_game_state.getNumAgents()):
                next_state = curr_game_state.generateSuccessor(curr_depth % curr_game_state.getNumAgents(), action)
                next_move, next_value = _AlphaBeta(next_state, alpha, beta, curr_depth + 1)  # recursive call
                if curr_depth % curr_game_state.getNumAgents() == 0:  # if player(pos) == MAX:
                    if value < next_value:
                        value, best_move = next_value, action
                    if value >= beta:
                        return best_move, value
                    alpha = max(alpha, value)
                else:  # if player(pos) == MIN:
                    if value > next_value:
                        value, best_move = next_value, action
                    if value <= alpha:
                        return best_move, value
                    beta = min(beta, value)

            return best_move, value

        return _AlphaBeta(gameState, -99999999, 99999999, 0)[0]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def _Expectimax(curr_game_state, curr_depth):
            best_move = None
            if curr_depth >= self.depth * curr_game_state.getNumAgents():
                return best_move, self.evaluationFunction(curr_game_state)

            if curr_game_state.isWin() or curr_game_state.isLose():
                return best_move, self.evaluationFunction(curr_game_state)  # terminal state!

            if curr_depth % curr_game_state.getNumAgents() == 0:  # player(pos) == MAX
                value = -99999999  # value = -infinity
            else:  # player(pos) == CHANCE
                value = 0  # value = 0

            for action in curr_game_state.getLegalActions(curr_depth % curr_game_state.getNumAgents()):
                next_state = curr_game_state.generateSuccessor(curr_depth % curr_game_state.getNumAgents(), action)
                next_move, next_value = _Expectimax(next_state, curr_depth+1)  # recursive call
                if curr_depth % curr_game_state.getNumAgents() == 0 and value < next_value:
                    value, best_move = next_value, action
                if curr_depth % curr_game_state.getNumAgents() != 0:
                    value += 1.0/len(curr_game_state.getLegalActions(curr_depth % curr_game_state.getNumAgents())) * next_value

            return best_move, value

        return _Expectimax(gameState, 0)[0]

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()

    foods = newFood.asList()
    for ghost_index in range(len(newGhostStates)):
        ghost = currentGameState.getGhostPosition(ghost_index + 1)
        if manhattanDistance(newPos, ghost) <= 1:
            # make sure the pacman is away from ghosts by giving a minimal score to such cases
            return -99999999

    if len(foods) == 0:
        return 1
        # no food left means winning, and we always go for win!

    #minimal_distance = 9999999
    #total_distance = 0
    distances = []

    for food_index in range(len(foods)):
        distance = manhattanDistance(foods[food_index], newPos)
        distances.append(distance)

    distances.sort()

    score = 0

    for i in range(len(distances)):
        if i > 4:
            break
        score -= distances[i] / (5 ** i)

    score -= 1000 * len(foods)

    return score
    # encourage the pacman to get more food by penalizing the score with more food left

# Abbreviation
better = betterEvaluationFunction

# qlearningAgents.py
# ------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

# from game import *
# from featureExtractors import *

import random, util, math
import time

import numpy as np

from displays import GuiDisplay


def exactQ(board, epsilon, gamma, alpha, numTraining, draw_board_after_policy=True):
    qLearningAgent = QLearningAgent(board, epsilon, gamma, alpha, numTraining)
    # state, result = qLearningAgent.playGame(reset_game=False, draw=False)
    start_time = time.time()
    learn = qLearningAgent.learn()
    time_taken = time.time() - start_time
    print('Time taken: ', round(time_taken, 3))

    action_list, result = qLearningAgent.adopt_policy(draw=True)
    if draw_board_after_policy:
        display = GuiDisplay(board.board_w, board.board_h, title='Intro to AI -- 67842 -- FlowFree')
        dots = [tup for sublist in [v.get_edges() for k, v in board.all_colors.items()] for tup in sublist]
        display.draw_board(board, dots=dots)
        time.sleep(0.5)
        for action in action_list:
            board.add_move(action)
            display.draw_board(board, dots=dots)
            time.sleep(0.5)
        time.sleep(10)
    return [time_taken, len(learn), bool(result)]


class QLearningAgent:
    """
      Q-Learning Agent

      Functions you should fill in:
        - getQValue
        - getAction
        - getValue
        - getPolicy
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions
          for a state
    """

    def __init__(self, board, epsilon, gamma, alpha, numTraining):
        self.board = board
        self.episodesSoFar = 0
        self.accumTrainRewards = 0.0
        self.accumTestRewards = 0.0
        self.numTraining = int(numTraining)
        self.epsilon = float(epsilon)
        self.alpha = float(alpha)
        self.discount = float(gamma)
        self.q_values = util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we never seen
          a state or (state,action) tuple
        """
        state_val = state.__str__()
        action_val = action.__str__()
        return self.q_values[(state_val, action_val)]

    def getValue(self, state, flag_q=True):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        max_val = -float('inf')
        all_actions = None if state is None else state.get_legal_moves(flag_q=flag_q)
        if not all_actions:
            return 0.0
        for actions in all_actions:
            q_val_action = self.getQValue(state, actions)
            if q_val_action > max_val:
                max_val = q_val_action
        return max_val

    def getPolicy(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        q_flag = True
        state_value = self.getValue(state, flag_q=q_flag)
        # possible_moves = state.get_legal_moves()
        possible_moves = state.get_legal_moves(flag_q=q_flag)
        all_actions = [action for action in possible_moves if self.getQValue(state, action) == state_value]
        if not all_actions:
            return None
        return random.choice(all_actions)

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        # legalActions = state.get_legal_moves()
        legalActions = state.get_legal_moves(flag_q=True)
        action = None
        if legalActions:
            choose_random = util.flipCoin(self.epsilon)
            if choose_random:
                action = random.choice(legalActions)
            else:
                action = self.getPolicy(state)
        return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        q_flag = True
        q_val = self.getQValue(state, action)
        q_next_val = self.getValue(nextState, flag_q=q_flag)
        state_val = state.__str__()
        action_val = action.__str__()
        self.q_values[(state_val, action_val)] = q_val + self.alpha * (reward + self.discount * q_next_val - q_val)

    def observeTransition(self, state, action, nextState, deltaReward):
        """
            Called by environment to inform agent that a transition has
            been observed. This will result in a call to self.update
            on the same arguments

            NOTE: Do *not* override or call this function
        """
        self.episodeRewards += deltaReward
        self.update(state, action, nextState, deltaReward)

    def startEpisode(self):
        """
          Called by environment when new episode is starting
        """
        self.lastState = None
        self.lastAction = None
        self.episodeRewards = 0.0

    def stopEpisode(self):
        """
          Called by environment when episode is done
        """
        if self.episodesSoFar < self.numTraining:
            self.accumTrainRewards += self.episodeRewards
        else:
            self.accumTestRewards += self.episodeRewards
        self.episodesSoFar += 1
        if self.episodesSoFar >= self.numTraining:
            # Take off the training wheels
            self.epsilon = 0.0  # no exploration
            self.alpha = 0.0  # no learning

    def isInTraining(self):
        return self.episodesSoFar < self.numTraining

    def isInTesting(self):
        return not self.isInTraining()

    def setEpsilon(self, epsilon):
        self.epsilon = epsilon

    def setLearningRate(self, alpha):
        self.alpha = alpha

    def setDiscount(self, discount):
        self.discount = discount

    def doAction(self, state, action):
        """
            Called by inherited class when
            an action is taken in a state
        """
        self.lastState = state
        self.lastAction = action

    def playGame(self, reset_game=False, draw=False, trackReward=False, game=None, draw_game=False):
        game = game if game else self.board
        state = game.__copy__()
        next_state = 1
        reward = 0
        action_list = []
        while next_state:
            action = self.getAction(state)
            if action is not None:
                action_list.append(action)
            new_board = state.__copy__()
            next_state = new_board.do_move(action)
            if next_state:
                path_blocked = next_state.check_if_path_blocked()
                if path_blocked:
                    next_state = None
            state_reward = self.getReward(state, action, next_state)
            self.update(state, action, next_state, state_reward)
            if trackReward: reward += self.getReward(state, action, next_state)
            if next_state:
                state = next_state.__copy__()
        result = 0
        if state.is_game_complete(): result = 1
        else: result = -1
        # if draw: state.draw()
        # if reset_game: self.game.game_state.reset()
        return state, result, action_list

    def getReward(self, state, action, nextState):
        if state.is_game_complete():
            return 500
        elif nextState is None:
            return -500
        elif nextState.is_game_complete():
            return 1000
        elif action.get_color() in nextState.completed_paths_colors:
            return 50 * len(nextState.completed_paths_colors) / state.num_of_colors
        elif action.get_color() not in [move.get_color() for move in nextState.get_legal_moves(flag_q=False)]:
            return -200
        else:
            return 0

    def learn(self):
        counter = 0
        win_counter = 0
        while counter < self.numTraining:
            end_state, game_result, _ = self.playGame()
            win_counter += game_result if game_result == 1 else 0
            if win_counter > 20:
                print('iteration: ', counter)
                return self.q_values
            counter += 1
        print('training done - won ' + str(100 * win_counter / counter) + '% of games')
        return self.q_values

    def adopt_policy(self, draw=False, game=None):
        game = game if game else self.board
        epsilon_store = self.epsilon
        self.epsilon = 0
        state, result, action_list = self.playGame(reset_game=False, game=game, draw_game=True)
        print('win') if result == 1 else print('loss')
        self.epsilon = epsilon_store
        return action_list, result

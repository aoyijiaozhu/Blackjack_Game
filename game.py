import random

# 定义牌类
class Card():
    def __init__(self ,suit ,rank):
        self.suit = suit
        self.rank = rank

    def show(self):
        print(f"{self.suit}{self.rank}")

# 定义牌堆类
class Deck():
    def __init__(self):
        self.cards = []
        self.build()

    # 创建牌堆，4副除了大小王的标准扑克
    def build(self):
        suits = ["黑桃", "梅花", "方块", "红心"]
        ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        for suit in suits:
            for rank in ranks:
                for _ in range(4):
                    self.cards.append(Card(suit ,rank))
        #self.cards.append((Card('', '小王')))
        #self.cards.append((Card('', '大王')))
        #for _ in range(len(self.cards)-1):
        #    self.cards[_].show()

    # 洗牌
    def shuffle(self):
        for i in range(len(self.cards ) -1 ,0 ,-1):
            r = random.randint(0 ,i)
            self.cards[i] ,self.cards[r] = self.cards[r] ,self.cards[i]
        for i in range(len(self.cards ) -1 ,0 ,-1):
            r = random.randint(0 ,i)
            self.cards[i] ,self.cards[r] = self.cards[r] ,self.cards[i]

    # 发牌
    def deal(self):
        return self.cards.pop()

# 定义玩家类
class Player():
    def __init__(self ,name):
        self.name = name
        self.hand = []

    # 摸牌
    def draw(self ,deck):
        self.hand.append(deck.deal())
        return self

    # 显示手牌
    def showHand(self):
        print(f"{self.name}'s hand:")
        for card in self.hand:
            card.show()

# 定义游戏类
class Game():
    def __init__(self):
        '''name1 = input("player1's name:")
        name2 = input("player2's name:")
        name3 = input("player3's name:")'''
        name1='player1'
        name2='player2'
        name3='player3'
        self.deck = Deck()
        self.player1 = Player(name1)
        self.player2 = Player(name2)
        self.player3 = Player(name3)

    def startGame(self):
        self.deck.shuffle()
        for i in range(2):
            self.player1.draw(self.deck)
            self.player2.draw(self.deck)
            self.player3.draw(self.deck)
        self.player1.showHand()
        self.player2.showHand()
        self.player3.showHand()

# 开始游戏
#game = Game()
#game.startGame()
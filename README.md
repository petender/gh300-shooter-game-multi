# 🎯 Reflex Shooter - Test Your Reaction Time!

A competitive arcade-style shooting game that tests your reflexes in thrilling head-to-head matches. Challenge yourself or compete with friends to see who has the fastest reaction time!

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.5+-green.svg)
![Built with GitHub Copilot](https://img.shields.io/badge/Built%20with-GitHub%20Copilot-purple.svg)

## 🎮 Game Features

### Core Gameplay
- **Lightning-Fast Reflexes**: Hit targets within 0.3 seconds to win
- **2-Player Competitive Mode**: Battle head-to-head with a friend
- **3 Rounds per Player**: Best of 3 determines the ultimate champion
- **Random Target Placement**: Every round is unique and unpredictable
- **Anti-Cheat System**: Early shots result in immediate disqualification

### Visual & Audio Experience
- 💥 **Explosive Animations**: Satisfying particle effects when you nail a target
- 🔊 **Dynamic Sound Effects**: Countdown beeps, explosions, and victory/defeat music
- 🎨 **Colorful Graphics**: Clean, arcade-style visuals with color-coded feedback
- ⚡ **Instant Feedback**: Real-time reaction time display

### Progression & Competition
- 📊 **Persistent High Scores**: Top 10 fastest times saved across sessions
- 🏆 **Game Summary Screen**: Detailed breakdown of all rounds
- 👑 **Winner Declaration**: Automatic champion announcement
- 📅 **Date-Stamped Records**: Track when records were set

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download this repository**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the game**:
```bash
python reflex_shooter.py
```

## 🎯 How to Play

1. **Enter Player Names**: Both players input their names
2. **Watch for the Countdown**: 3... 2... 1... GET READY!
3. **Wait for the Target**: A red and white bullseye appears randomly
4. **Press SPACE**: Shoot as fast as you can!
5. **Check Your Time**: Win if you're under 0.3 seconds
6. **Compete**: Alternate between players for 3 rounds each
7. **View Results**: See the winner and check the high scores

### ⚠️ Pro Tips
- **Don't shoot early!** Pressing space before the target appears results in instant disqualification
- **Stay focused** during the random delay after "GET READY"
- **Best time wins** - even if you lose individual rounds, your fastest shot counts!

## 🏗️ Built Entirely with GitHub Copilot

This entire game was created using **GitHub Copilot** as an AI pair programmer! Every feature, from the core gameplay to sound effects and high scores, was developed through natural language prompts and AI-assisted coding.

### 🤖 Sample Prompts Used

Want to build this game yourself with GitHub Copilot? Here are the exact prompts used:

#### Initial Game Setup
```
as a kid, I played arcade games a lot. I want to build a Python app, which tests me on my shooting reflexes. Help me developing a game which does the following:

1. aks for player name input
2. bottom middle of the game screen shows a shooter 
3. anywhere random on screen appears a target
4. player uses the space bar to simulate a shoot
5. calculate the time between the target appearing and player pressing the space bar to shoot
6. if that time is less than 0.3 sec, player wins, otherwise computer wins
7. show a "YOU WIN" or "YOU ARE TOO SLOW" depending on the outcome 

From there, I will test the game play, and confirm it all works as expected. Once I confirm, you can update the game in such a way that it allows for 2 players, and also saves the high scores in a table view. Each player should have 3 rounds of play, switching players for each play.
```

#### Adding Anti-Cheat Protection
```
ok, base game functionality works. apart from the additional features, can you also build in a scenario where - if the player presses the spacebar before the target is loaded, they immediately lose? as I found a little hack that would allow me to win if I press the spacebar enough during game loading
```

#### Enhancing with Audio-Visual Effects
```
ooh sound effects... yes please! and since we're at it, can you add some additional graphical elements that shows an exploded target when hit?
```

#### Project Organization
```
can you create a pip requirements file with the necessary packages, so it's easier to reinstall
```

## 📁 Project Structure

```
pygame/
├── reflex_shooter.py      # Main game file
├── requirements.txt       # Python dependencies
├── high_scores.json      # Persistent high scores (auto-generated)
└── README.md             # This file
```

## 🛠️ Technical Details

### Technologies Used
- **Python**: Core programming language
- **Pygame**: Game framework for graphics and input handling
- **NumPy**: Audio signal generation for sound effects
- **JSON**: High score persistence

### Key Features Implementation
- **Sound Generation**: Procedurally generated sine waves and noise for all audio
- **Particle System**: Custom explosion animation with 12 radiating particles
- **Event-Driven Architecture**: Clean input handling with anti-cheat detection
- **Data Persistence**: JSON-based high score storage with date tracking

## 🎨 Game Mechanics

### Reaction Time Scoring
- **< 0.3 seconds**: YOU WIN! ✅
- **≥ 0.3 seconds**: YOU ARE TOO SLOW ❌
- **Early shot**: TOO EARLY! (999.0 penalty time) ⚠️

### Winning Condition
The player with the **fastest single reaction time** across all 3 rounds wins the match!

## 🏆 High Scores

The game automatically tracks the top 10 fastest reaction times of all time. Scores are saved to `high_scores.json` and persist between sessions.

### High Score Display Features
- Rank (1-10)
- Player Name
- Reaction Time (in seconds)
- Date/Time Achieved
- Top 3 highlighted in cyan

## 🤝 Contributing

This project was created as a demonstration of AI-assisted development with GitHub Copilot. Feel free to:
- Fork the repository
- Add new features
- Create your own variations
- Share your improvements

## 📝 License

This project is open source and available for educational and personal use.

## 🎓 Learning Resources

Want to build games like this using GitHub Copilot?
- Learn how to write clear, descriptive prompts
- Break complex features into smaller tasks
- Iterate and refine based on testing
- Use natural language to describe desired functionality

## 🙏 Acknowledgments

- **GitHub Copilot**: For being an amazing AI pair programmer
- **Pygame Community**: For excellent documentation and examples
- **Arcade Gaming**: For inspiring this nostalgic project

---

**Ready to test your reflexes? Fire up the game and see if you can make it to the high scores!** 🎯🔥

*Built with ❤️ and GitHub Copilot*

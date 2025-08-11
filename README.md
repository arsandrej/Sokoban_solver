# Sokoban Solver with AI & Graphical Interface

A **Sokoban** puzzle game with both manual play and AI solvers, implemented in Python using **Pygame**.  
This project features **deadlock detection**, multiple solving algorithms (**A\***, **BFS**, **DFS**), solution visualization, and customizable themes.

## 🕹️ Game Goal
Sokoban is a logic puzzle where the player pushes boxes onto goal positions.
- **You win** when **all boxes** are placed on the goal tiles.
- Boxes can **only be pushed**, not pulled.
- The player cannot walk through walls or boxes.
- The challenge lies in avoiding **deadlock states** where the puzzle becomes unsolvable.

## 🎯 Project Goals
The aim of this project is to:
- Implement **AI algorithms** capable of solving Sokoban efficiently.
- Compare solver performance using metrics like **execution time** and **nodes explored** between different algorithms.
- Explore **game-specific optimizations** such as deadlock detection and heuristics.
- Provide a **graphical interface** for interactive play and AI solution visualization.

## 📦 Features

### 🧠 AI Solvers
- **A\***, **BFS**, and **DFS** search algorithms.
- **Solution statistics**: execution time, explored nodes.
- **Deadlock detection**:
  - Corner deadlocks
  - Wall deadlocks
  - Tunnel deadlocks
  - Freeze deadlock
- **Heuristics**:
  - Manhattan and Euclidean distances
  - **Hungarian algorithm** for optimal box-goal matching

### 🎨 Graphics & UI
- Built with **Pygame** for a simple solving algorithm representation.
- **Multiple visual themes**: blue, red, brown, gray.
- Basic rendering for player, boxes, walls, and goals.
- **Solution playback** with adjustable animation speed.

### 🎮 Game Modes
- **Play Solo**: Manual gameplay with undo/reset.
- **AI Solver**: Watch and compare AI solver performances.
- **Settings Menu**: Choose themes, Select Different levels.


# CS50AI Problem Set Solutions

This repository contains my solutions to the problem sets from CS50’s Introduction to Artificial Intelligence with Python, an online course offered by Harvard University. The course covers fundamental AI concepts and their implementation using Python, including search algorithms, optimization techniques, machine learning, and reinforcement learning.

📌 Course Overview

CS50AI explores various AI techniques, focusing on:
	•	Search Algorithms: Depth-First Search (DFS), Breadth-First Search (BFS), A* Search
	•	Knowledge Representation: Propositional Logic, Inference
	•	Uncertainty & Probability: Bayesian Networks
	•	Machine Learning: Supervised & Unsupervised Learning, Neural Networks
	•	Optimization: Constraint Satisfaction Problems
	•	Reinforcement Learning: Markov Decision Processes, Q-learning
	•	Natural Language Processing (NLP): Tokenization, N-grams, Sentiment Analysis

📂 Repository Structure

Each problem set is stored in its respective directory, containing the problem description and my implementation.

📦 CS50AI  
 ┣ 📂 0-search  
 ┃ ┣ 📁 degrees   
 ┃ ┗ 📁 tictactoe    
 ┣ 📂 1-knowledge  
 ┃ ┣ 📁 minesweeper  
 ┃ ┗ 📁 knights  
 ┣ 📂 2-uncertainty  
 ┃ ┣ 📁 pagerank  
 ┃ ┗ 📁 heredity   
 ┣ 📂 3-optimization  
 ┃ ┗ 📁 crossword  
 ┣ 📂 4-learning  
 ┃ ┣ 📁 shopping  
 ┃ ┗ 📁 nim   
 ┣ 📂 5-neural-networks  
 ┃ ┗ 📁 traffic   
 ┣ 📂 6-language  
 ┃ ┣ 📁 parser  
 ┃ ┗ 📁 attention    
 ┗ 📜 README.md  

🚀 Getting Started

Prerequisites

Ensure you have Python 3 installed. You may also need additional libraries such as NumPy, Pandas, and TensorFlow for certain problem sets. Install dependencies using:

pip install -r requirements.txt

Running the Solutions

Each directory contains Python scripts that implement the solutions. You can run them using:

python filename.py

For example, to run the degrees problem in 0-search/degrees/ :

python degrees.py

🛠 Technologies Used
	•	Python 3
	•	AI Algorithms (Search, CSPs, Probabilistic Models, etc.)
	•	Machine Learning Frameworks (Scikit-learn, TensorFlow)
	•	Natural Language Processing (NLP)


⚠️ I’ve removed some files to optimize the repository size. Specifically:
	•	In the degrees folder, the large and small datasets have been removed. You can download them from:
📥 Download Degrees Dataset: https://cdn.cs50.net/ai/2023/x/projects/0/degrees.zip
	•	In the traffic folder, the gtsrb dataset has been removed. You can download it from:
📥 Download GTSRB Dataset: https://cdn.cs50.net/ai/2023/x/projects/5/gtsrb.zip

Make sure to extract and place these datasets in their respective directories before running the related scripts.

📜 License

This repository is intended for educational purposes only. Please refrain from copying solutions directly if you’re currently taking the CS50AI course.

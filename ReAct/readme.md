# ReAct Framework Implementation

This project implements the ReAct (Reasoning and Acting) framework as described in the paper ["ReAct: Synergizing Reasoning and Acting in Language Models"](https://arxiv.org/abs/2210.03629). The implementation enables an AI assistant to solve complex problems by alternating between reasoning steps and actions.

## Table of Contents
- [ReAct Framework Implementation](#react-framework-implementation)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Project Structure](#project-structure)
  - [Implementation Details](#implementation-details)
    - [main.py](#mainpy)
      - [Key Components:](#key-components)
    - [WikiTool.py](#wikitoolpy)
    - [promptTemplate.py](#prompttemplatepy)
  - [How It Works](#how-it-works)
  - [Example Interactions](#example-interactions)
    - [Example 1: Simple Fact Retrieval](#example-1-simple-fact-retrieval)
    - [Example 2: Multi-step Reasoning](#example-2-multi-step-reasoning)
  - [Setup and Installation](#setup-and-installation)
  - [Usage](#usage)
  - [Extending the Framework](#extending-the-framework)
    - [Adding New Tools](#adding-new-tools)
    - [Improving the Prompt](#improving-the-prompt)
    - [Performance Optimization](#performance-optimization)
  - [References](#references)

## Overview

ReAct is a framework that combines reasoning (thinking through a problem) and acting (taking actions to gather information). This implementation uses OpenAI's language models to perform reasoning and Wikipedia as an external knowledge source for actions.

The core concept is to allow the AI to:
1. Think about what information it needs
2. Take actions to gather that information
3. Incorporate the observations into its reasoning
4. Continue this process until it can provide a complete answer

## Project Structure

```
Agents/
├── main.py              # Main execution logic
├── WikiTool.py          # Wikipedia interaction tool
├── promptTemplate.py    # System instructions and examples
├── .env                 # Environment variables (API keys)
└── README.md            # This documentation
```

## Implementation Details

### main.py

The main script contains the core logic of the ReAct framework:

#### Key Components:

1. **Initialization**
   - Loads environment variables from `.env`
   - Sets up the OpenAI client
   - Initializes the Wikipedia tool

2. **Action Parsing**
   - `parse_action()`: Extracts action type and query from the AI's response using regex
   - Supports two action types: `search` and `lookup`

3. **ReAct Loop**
   - `run_react_loop()`: Implements the main interaction loop
   - Maintains conversation history
   - Processes the AI's responses
   - Executes actions and records observations
   - Terminates when a final answer is provided

```python
def run_react_loop(question):
    wiki_tool = WikiTool()
    history = f"{SYSTEM}\n{EXAMPLES}\n# New Question\nQuestion: {question}"
    observation_count = 0
    
    while True:
        # Get AI response
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": history}],
            temperature=0.0
        )
        content = response.choices[0].message.content.strip()
        print("AI:", content)
        
        # Handle different response types
        if content.startswith("Action"):
            # Process action and get observation
            observation_count += 1
            action_type, action_query = parse_action(content)
            if action_type == "search":
                obs = wiki_tool.search(action_query)
            elif action_type == "lookup":
                obs = wiki_tool.lookup(action_query)
            else:
                obs = "Invalid action. Please use search[\"query\"] or lookup[\"page\"]."
            
            # Add observation to history
            history += f"\n{content}\nObservation {observation_count}: {obs}"
            
        elif content.startswith("Thought"):
            # Record thought without response
            history += f"\n{content}"
            
        elif content.startswith("Final Answer"):
            # Present final answer and exit
            print("\nFinal Answer:", content.replace("Final Answer:", "").strip())
            break
            
        else:
            # Handle unexpected format
            history += f"\n{content}\nObservation {observation_count}: Please follow the format: Thought, Action, or Final Answer."
```

### WikiTool.py

This module provides the interface to Wikipedia:

```python
class WikiTool:
    def __init__(self):
        user_agent = "ReAct-Agent/1.0 (For research purposes; contact: your-email@example.com)"
        self.wiki_wiki = wikipediaapi.Wikipedia(user_agent=user_agent, language='en')
    
    def search(self, query):
        """
        Search for a query in Wikipedia and return the summary of the first result.
        """
        page = self.wiki_wiki.page(query)
        if page.exists():
            return page.summary
        else:
            return f"No results found for '{query}'."
    
    def lookup(self, page):
        """
        Look up a specific page in Wikipedia and return its summary.
        """
        wiki_page = self.wiki_wiki.page(page)
        if wiki_page.exists():
            return wiki_page.summary
        else:
            return f"No results found for '{page}'."
```

The `WikiTool` class provides two methods:
- `search(query)`: Searches for information about a topic
- `lookup(page)`: Retrieves detailed information about a specific Wikipedia page

Both methods return summaries of Wikipedia articles, which are then provided to the AI as observations.

### promptTemplate.py

This file contains two important string templates:

1. **SYSTEM**: Defines the AI's role, available actions, and expected response format
2. **EXAMPLES**: Provides examples of the ReAct process to guide the AI's behavior

The system prompt is crucial for instructing the AI on how to format its responses:

```
You are an AI assistant that answers complex questions by reasoning step by step and using Wikipedia when needed.

You have two actions available to help with research:
1. search["query"] - Search for information about a topic
2. lookup["page"] - Look up a specific Wikipedia page

Always follow this process:
1. Think about what information you need to answer the question
2. Use search or lookup actions to gather information
3. Continue thinking and searching until you have enough information
4. Provide a Final Answer

Format your responses like this:
Thought N: Your reasoning
Action N: search["query"] or lookup["page"]
(The system will then provide an Observation)
Final Answer: Your complete answer to the question
```

The examples demonstrate the expected interaction pattern with complete workflows showing thoughts, actions, observations, and final answers.

## How It Works

1. **Initialization**: The system sets up the environment and tools.
2. **User Question**: The user provides a question.
3. **ReAct Loop**:
   - The AI generates a thought about what information it needs.
   - The AI takes an action (search or lookup) to gather information.
   - The system executes the action and returns an observation.
   - The AI incorporates this information into its reasoning.
   - This process repeats until the AI has enough information.
4. **Final Answer**: The AI provides a complete answer to the original question.

## Example Interactions

### Example 1: Simple Fact Retrieval

```
Question: What university did Emma Watson attend?

Thought 1: I need to search for information about Emma Watson to find out which university she attended.
Action 1: search["Emma Watson"]
Observation 1: Emma Charlotte Duerre Watson (born 15 April 1990) is an English actress and activist. She is known for her roles in both blockbusters and independent films, as well as for her women's rights work. Watson attended Dragon School and trained as an actress at the Oxford branch of Stagecoach Theatre Arts. She rose to prominence after playing Hermione Granger in the Harry Potter film series. She attended Brown University and Worcester College, Oxford.

Thought 2: According to the search results, Emma Watson attended Brown University and Worcester College, Oxford.
Final Answer: Emma Watson attended Brown University and Worcester College, Oxford.
```

### Example 2: Multi-step Reasoning

```
Question: Who was the director of the movie that had Leonardo DiCaprio as an FBI agent?

Thought 1: I need to find movies where Leonardo DiCaprio played an FBI agent.
Action 1: search["Leonardo DiCaprio FBI agent movie"]
Observation 1: Leonardo DiCaprio has played an FBI agent in the 2002 film "Catch Me If You Can" directed by Steven Spielberg, where he co-starred with Tom Hanks. DiCaprio played Frank Abagnale Jr., who was pursued by an FBI agent, not an FBI agent himself. In the 2011 film "J. Edgar" directed by Clint Eastwood, DiCaprio played J. Edgar Hoover, the first Director of the FBI.

Thought 2: Based on the search, Leonardo DiCaprio played J. Edgar Hoover, the first Director of the FBI, in the movie "J. Edgar" directed by Clint Eastwood. Let me verify this information.
Action 2: lookup["J. Edgar (film)"]
Observation 2: J. Edgar is a 2011 American biographical drama film directed by Clint Eastwood and written by Dustin Lance Black. The film focuses on the career of FBI director J. Edgar Hoover from the Palmer Raids onwards. The film stars Leonardo DiCaprio as the title character, Armie Hammer, Naomi Watts, Josh Lucas, and Judi Dench.

Thought 3: The information is confirmed. Leonardo DiCaprio played J. Edgar Hoover, who was the FBI director, in the movie "J. Edgar" directed by Clint Eastwood.
Final Answer: Clint Eastwood was the director of the movie "J. Edgar" in which Leonardo DiCaprio played J. Edgar Hoover, the first Director of the FBI.
```

## Setup and Installation

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd Agents
   ```

2. **Install dependencies**:
   ```
   pip install openai tiktoken wikipedia-api python-dotenv rich
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root with:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

Run the main script and enter your question when prompted:

```
python main.py
```

## Extending the Framework

### Adding New Tools

You can extend the ReAct framework by adding new tools:

1. Create a new tool class (e.g., `CalculatorTool.py`)
2. Implement methods for the actions you want to support
3. Add the new action types to the system prompt
4. Update the `parse_action()` function to recognize the new actions
5. Update the main loop to handle the new actions

### Improving the Prompt

The quality of responses largely depends on the system prompt and examples:

1. Add more diverse examples to cover different types of questions
2. Refine the system instructions to guide the AI's behavior
3. Experiment with different formats for thoughts and actions

### Performance Optimization

For better performance:

1. Implement caching for Wikipedia queries to reduce API calls
2. Add timeout handling for external API calls
3. Implement error handling for failed actions

## References

- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [Wikipedia API Documentation](https://pypi.org/project/Wikipedia-API/)
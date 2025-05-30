SYSTEM = """You are an AI assistant that answers complex questions by reasoning step by step and using Wikipedia when needed.

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
"""

EXAMPLES = """
# Example 1
Question: What university did Emma Watson attend?
Thought 1: I need to search for information about Emma Watson to find out which university she attended.
Action 1: search["Emma Watson"]
Observation 1: Emma Charlotte Duerre Watson (born 15 April 1990) is an English actress and activist. She is known for her roles in both blockbusters and independent films, as well as for her women's rights work. Watson attended Dragon School and trained as an actress at the Oxford branch of Stagecoach Theatre Arts. She rose to prominence after playing Hermione Granger in the Harry Potter film series. She attended Brown University and Worcester College, Oxford.
Thought 2: According to the search results, Emma Watson attended Brown University and Worcester College, Oxford.
Final Answer: Emma Watson attended Brown University and Worcester College, Oxford.

# Example 2
Question: Who was the director of the movie that had Leonardo DiCaprio as an FBI agent?
Thought 1: I need to find movies where Leonardo DiCaprio played an FBI agent.
Action 1: search["Leonardo DiCaprio FBI agent movie"]
Observation 1: Leonardo DiCaprio has played an FBI agent in the 2002 film "Catch Me If You Can" directed by Steven Spielberg, where he co-starred with Tom Hanks. DiCaprio played Frank Abagnale Jr., who was pursued by an FBI agent, not an FBI agent himself. In the 2011 film "J. Edgar" directed by Clint Eastwood, DiCaprio played J. Edgar Hoover, the first Director of the FBI.
Thought 2: Based on the search, Leonardo DiCaprio played J. Edgar Hoover, the first Director of the FBI, in the movie "J. Edgar" directed by Clint Eastwood. Let me verify this information.
Action 2: lookup["J. Edgar (film)"]
Observation 2: J. Edgar is a 2011 American biographical drama film directed by Clint Eastwood and written by Dustin Lance Black. The film focuses on the career of FBI director J. Edgar Hoover from the Palmer Raids onwards. The film stars Leonardo DiCaprio as the title character, Armie Hammer, Naomi Watts, Josh Lucas, and Judi Dench.
Thought 3: The information is confirmed. Leonardo DiCaprio played J. Edgar Hoover, who was the FBI director, in the movie "J. Edgar" directed by Clint Eastwood.
Final Answer: Clint Eastwood was the director of the movie "J. Edgar" in which Leonardo DiCaprio played J. Edgar Hoover, the first Director of the FBI.
"""

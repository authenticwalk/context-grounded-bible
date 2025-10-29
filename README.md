# Overview

We are attempting to create the largest AI readable commentary on the entire Bible to empower 
Bible translators, pastors and students to use AI effectively and accurately.  The problem with AI
(more specifically text prediction models like chatGPT) is they are more poet than academic. Their
goal is to make the next word sound correct in light of all the data that came before it.  It 
doesn't want to leave any of your questions unanswered so like the friend who always has an answer it
answers confidently but not always grounded in truth.

# Solution

Since it is creating the next word on the importance of the words before we add to those words before 
the actual text and considerations.  Since computers can read and hold in memory an entire book in under
1 second we provide a books worth of information for every verse in the Bible. 

The reason this is important is because the AI is inconsistent.  When it was trained it read the entire Internet
and several million books.  Fortunately for us one of the most common books is the Bible so it knows it fairly
well.  It was given a phrase like "in the beginning was " and it had to predict the next word.  The more it encountered "in the beginning was God" from Geneis or the other option from John "in the beginning was the word" the more it was rewarded for getting it right.  It learnt that when it was in Genesis to use the first and the latter when in discussion about John.  In so doing it essentially compressed the entire Internet and human knowledge.  

So if you ask AI about something common like John 3:16 it has seen a lot and appears to answer accurately.  If you get other texts it is still fairly good with NIV, KJV, etc because those appear on the Internet so many times.  If you move to lesser quoted texts like the minor prophets or numbers you get lesser results.  If you use those same texts in rare languages you begin to get words strung together that look good but may be "lossy" (to use the compression analogy).  This begins to get dangerous as it sounds just as confident about the things it actually knows a lot about and if users fail to fact-check the sources they will clumbsily be mislead or mislead.

So we fix this by providing extensive context so it is grounded in truth.  

# Structure

We give an AI agent a task like "lookup all the original greek words for this verse" and it will process this
verse by verse till it is finished the entire Bible.

These are stored as YAML files which are both human and AI readable in the directory

`./bible/{book}/{chapter}/{verse}/{book}-{chapter}-{verse}-{task}.yaml`

The data is loosely structured so it could be merged and filtered

# Questions we are seeking to answer

The following are some tasks we are proposing to have AI answer

 - [ ] What are all the Greek words in this text
 - [ ] What are the unique nuances of each Greek word in the context of this verse
 - [ ] How do different Bible translations translate this across not only English but all 1000 languages? Group them by the nuances of the original word.  Highlight any unique cultural words that are rich in meaning.
 - [ ] How can this verse be segmented into key groups like "kingdom of God" that need to be translated together
 - [ ] How does this verse compare to other similar verses.  For example Matthew "poor in spirit" vs just "poor"
 - [ ] What are the different interpretations of this verse?  What implications do they have?
 - [ ] How have pastors taught on this verse, what outline have they used, key illustrations, main points.
 - [ ] What movie clips, novels, historical events, art illustrate this verse well

# Creating Data

This project uses claude code as an AI agent to handle it, you can see how it does it in the ./claude folder

To install it go to your terminal in your computer OR https://claude.ai/code

`npm install -g @anthropic-ai/claude-code`

`claude`

The agent works like this

 1. Human asks AI a question like "what are all the Greek words used in every verse"
 2. The AI clarifies the goals with various possibilities and waits for human feedback
 3. The AI attempts to create a data file for this task on a random Scripture and requests feedback
 4. The human and another AI agent provide feedback on what is useful, accurate, etc
 5. The AI refines it's own instructions to improve the results, cylcing back through steps 3-5 until it can gain no further improvements (self-learning loop)
 6. It then processes the entire Bible

# Using the Data

## Script

The simplest way is to just get all the data for a verse

`cat ./bible/MAT/5/3/*.yaml > merged.yaml`

## MCP (future)

With most AI agents like chatGPT you can add an MCP server so AI can talk to other sources.  In this case
when you add the MCP tool it will tell the AI to get this data whenever working on a verse.

## Subagent (future)

The data will eventually get really big and fill your context window.  So it will be better to have your AI agent call a subagent to study a bible verse who in turn calls the MCP or the script.
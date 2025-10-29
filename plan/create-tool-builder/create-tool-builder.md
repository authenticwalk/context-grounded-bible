# Task

Your task will be to create a claude agent.  Here are some of the tasks you must do

 - [ ] Switch to the branch test/skill-in-skill-test
 - [ ] Create a new branch feat/subagent-create-skill
 - [ ] Research and Plan
 - [ ] Draft the initial README.md and LEARNINGS.md files
 - [ ] Deploy 5 subagents to run an experiment, these subagents should have their own agent file so they can have their data.

# Planning Phase

 - [ ] Review this project, find all files ending in *.md; focus on ./README.md ./todo.md SCHEMA.md and ./skills/bibel-study-tool-creator - record your findings in /plan/feat-subagent-create-skill/
 - [ ] Review best practices by doing web searches about claude code agents and create cheat sheet for this project into plan/research/claude-agents-research.md
 - [ ] Likewise do web searches on claude code skills and do a pro/con analysis of if this should be a skill or an agent
 - [ ] Spawn 5 subagents to review your plan from different perspectives and offer pros and cons of your approach and alternatives
 - [ ] Finalize your plan with the feedback, you will not incorporate all of it, focus on simplicity

# Scope

The following must be accomplished by the agent

 - [ ] It must create a folder in ./bible-study-tools/{tool-name}
 - [ ] it must create a file ./bible-study-tools/{tool-name}/README.md that has
  - [ ] a human readable title which is the name of the tool
  - [ ] an overview/description of the high level purpose of the tool.  Start with Why.  Specifically why it *must* exist to accomplish the project goals.  Then a quick summary of the how
  - [ ] 7 exceptionally clear, diverse and helpful examples of how the tool found an incredible insight, what the insight was and why this is important, these should be in long-form text description style of max 5 lines each
   - [ ] A schema following the semi-structured format in SCHEMA.md, this will be the tool output
- [ ] a file ./bible-study-tools/{tool-name}/LEARNINGS.md which will form a log in markdown format that the system continues appends to.  Subheading of experiment name with thesis/goal of experiment and the analysis (what worked, what didn't) with a link to the output file of ./bible-study-tools/{tool-name}/learnings-{experiment-name}-log/{BOOK}-{CH}-{VS}.yaml

 # Subagent - run tool experiment
 - [ ] Given a ./bible-study-tools/{tool-name}/README.md read it
 - [ ] Given an experiment (provided by the calling agent) 
 - [ ] Load the SCHEMA.md with your changes into  ./bible-study-tools/{tool-name}/learnings-{experiment-name}-log/rev1/README.md
 - [ ] Build the YAML schema file using whatever websearches and tools necessary for the following verses; you must do them one at a time and record each in the folder, spawn a subagent ( for each of these
   - [ ] John 1:1
   - [ ] Matthew 5:3
   - [ ] Col 3:1
   - [ ] Jn 11:35
   - [ ] Hab 3:9
   - [ ] Job 38:36
   - [ ] Ps 119:105
   - [ ] Dan 9:25
   - [ ] 1 Sam 15:3
   - [ ] Gen 36:11
- [ ] Spawn 5 subagents of the type of "reviewer" given 5 different but relevant personas of "Doctor of Theology", "Veteran Translator", "Principal Database engineer (focused on structure of data)", "1st year Bible college student", "pastor working on a sermon", "local underequipped translator")
- [ ] Evaluate the validity and importance of their feedback, throwing out the noise and finding the most important points.  Record that in ./bible-study-tools/{tool-name}/learnings-{experiment-name}-log/LEARNINGS.md
- [ ] Copy and Modify your ./bible-study-tools/{tool-name}/learnings-{experiment-name}-log/rev1/README.md file to attempt to fix those issues as  ./bible-study-tools/{tool-name}/learnings-{experiment-name}-log/rev2/README.md
- [ ] Reload your agent instructions in case you encountered context compression and lost where you were
- [ ] Repeat the step of building the YAML file for each verse, but now for only the problematic verses, add other verses that may also have problems, followed by the steps after it till either A) the reviewers are happy or B) max of 7 loops
 - [ ] Reread all the LEARNINGS.md for each revision and synthesize it into your key learnings in  ./bible-study-tools/{tool-name}/LEARNINGS.md with your experiment name.  Focus on what worked really well and what worked poorly including helpful websites, helpful techniques, schema fields, prompt engineering. 
 - [ ] If there is an absolutely steller insight found in the verses add it to the examples in  ./bible-study-tools/{tool-name}/README.md

# Subagent: Reviewer
 - [ ] Given a README.md in the target directory file descibing the task that was to be done and goals and a persona from your caller
 - [ ] Foreach file in the  target directory determine how helpful it was, saving it to a single file ./bible-study-tools/{tool-name}/learnings-{experiment-name}-log/{researcher-name}-{round}.md where round defaults to 1 but increments if there already is a file
   - [ ] Which insights would make a meaninful difference in your life or work, you are so thankful
   - [ ] Which sections could be removed as noise?
   - [ ] What looks inaccurate, possibly made up, or fake new/stories, even things people keep repeating online but are likely not true.
 - [ ] Aggregate all your findings into a shorter summary and return that as your final answer.


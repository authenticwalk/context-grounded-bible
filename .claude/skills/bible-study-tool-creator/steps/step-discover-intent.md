# STEP: Discover the Users Intent

## Step: Collect the input

The input may come from

 - a slash command parameter calling this skill
 - a skill being called with details
 - you can ask them what it is they want to make

First, check if the user already described what tool they want to create when invoking the skill. Look for context like:
- "create a tool to provide all the greek words for each verse"
- "I want to summarize Matthew Henry's Commentary"
- "analyze cultural metaphors across different translations"

**If the user already provided a description**: Capture that intent and proceed to SubStep 2.

**If no description was provided**: Brainstorm concrete tool ideas based on the project's mission to help Bible translators, pastors, and students.  You should have already done a ls -la of ./bible-study-tools when you checked for duplicates, *NEVER* suggest a tool that already exists.  Brainstorm similar ideas.  Then present them as options using AskUserQuestion:

```
Question: "What would you like this Bible study tool to do?"
Options (brainstorm 3-4 specific, valuable ideas):
- Extract Greek/Hebrew words with their definitions; focusing on the unique meaning in this verse
- Compare cultural adaptations of metaphors across minority language translations
- Analyze commentaries for key points about this verse
- Find movie clips, stories and other art that would illustrate this verse really well
- Other (I have a different idea)
```

When brainstorming ideas, focus on:
- Tasks that address real translation/interpretation challenges
- Analysis that LLMs can't do well from memory alone
- Data that would genuinely help translators/pastors/students

If user selects "Other", ask them to describe their idea in their own words.

Store their response as the initial tool concept.



### SubStep 2: Search for Existing Tools

Before proceeding, search for existing tools that might already do what the user wants. This avoids duplication.

**Check the directory**:
```bash
ls -la ./bible-study-tools/
```

**For each existing tool**, read its `README.md` and check if it matches the user's intent:
- What does it do?
- What are its goals?
- How does it differ from what the user described?

**If tools match**: list them in a AskUserQuestion tool with the name for the description compare it's description/goals to the users.  Your dialogue will be "There are several tools similar to this, which one do you want to work on?"  The final option is explain how yours is unique

**If no match found**: Proceed with creation.

### SubStep 2b: Refine the edit they want to make 

If they are choosing to edit a tool carefully look through the tools `README.md` and `LEARNING.md` and determine if there are suggestions in there of creating a similar tool.  Find the most relevant and potentially helpful and suggest those with the last option being to edit this tool itself.

## The Task is singular focused

We want the tool to be singular focused simpilar to how a PR in git would be singular focused.
This tool will generate a file which can then be merged with other tools files.  

Good examples

 - List all the source language words used in this verse
 - List all the words used in a language and all verses that use them with the related words in the gateway langauges that relate to this word
 - Break this verse down into semantic groups like "kingdom of God"
 - research 7 leading commentaries on this verse

Bad 
 - List all the source language words and how it relates to any word in every other language followed by a detailed analysis of that other language word (*NOTE* far too denormalized and would be very big, better to do the first part then do a file for each language to keep it clean)
 - break this verse down into all it's word, semantic groups, create an outline and illustrations (*NOTE* this could be several tasks)

## Guideline: Group by Purpose, Not by Source

**Think about how the data will be used.** If you'd naturally load multiple sources together for a task, they belong in the same file.

**Examples:**
- "I want lexical data" → includes Strong's, Young's, all concordances in one file
- "I want commentary insights" → may include multiple commentaries if they're small, or split if large
- "I want cultural context" → includes all cultural analysis sources
- "I want translation patterns for Spanish" → all Spanish translation data together

**When to split into separate files:**
- Content size gets too large (practical limit)
- Different focus areas (lexical vs theological vs cultural vs linguistic analysis)
- You wouldn't naturally load them together for the same task

**Key question to ask:** "Would someone using this data naturally want these sources together?"
- Yes → combine them (e.g., all lexical/concordance data)
- No → split them (e.g., lexical data vs commentary insights)

## SubStep 3: Clarify the foreach output scope for the data

**CRITICAL**: You must explicitly determine and document the foreach scope. This is NOT optional.

All of the tools will eventually become a foreach loop:
 - foreach verse (most common - generates one YAML file per verse)
 - foreach chapter (generates one YAML file per chapter)
 - foreach book (generates one YAML file per book)
 - foreach word (lexical analysis)
 - foreach language and word (translation mapping)
 - foreach topic (thematic analysis)
 - foreach book → writes to verse files (commentary that processes books but outputs to verses)
 - foreach topic → writes to verse files (thematic data that outputs to verses)

You can see examples and if we added new foreach loops in the project root todo.md

**Examples:**
- Analyze word root & etymology: **BAD** (missing what language, assuming the source language)
- Analyze source language (Greek, Hebrew) word root & etymology: **GOOD** (nice and clear)
- Map semantic word groups: **BAD** (for what?)
- Map semantic word groups foreach verse: **GOOD**
- Add Strong's numbers: **INCOMPLETE** (is this just Strong's, or all lexical/concordance data?)

**After determining scope, document it clearly** - it will be saved in step 2 after the tool name is chosen.

This ensures the foreach scope is explicitly determined and not lost during the workflow. 

## Make sure it is specific enough

If they say something like "I want to add sermon illustrations" that could be a broad task and valuable to break down into smaller units (see Group by Purpose)

It would be good to show them some options of how they will get the sermon illustrations
 - from movie clips, novels, art
 - review 100 sermons foreach verse and list the top illustrations used
 - go through my sermons on Google Drive and find the illustrations I have used
 - (Suggest a different method)

## Make sure it is broad enough to be useful

If they say "Let's add strong's number to every verse" we may want to show them multiple selects of
other commentaries and then a second tab of things you could do with lexical data.

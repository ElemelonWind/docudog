## Inspiration

As struggling EECS 281 students and avid StackOverflow surfers, we realized that we spend way too much time on documentation websites; skimming, rubbing our eyes, skimming with a bit more stringency, and then giving up. 

## What it does

Our app, DocuDog, allows users to input a link to any piece of documentation (or even a spec) that they are having trouble understanding. We scrape any associated links from the original link, then input all of the data into Gemini 1.5, instructing it to learn the specific information in those links so that the user can have a tailored chatbot experience. "How do you center text" turns into a much more specific query if the user inputs the Tailwind documentation before asking.

## How we built it

We built this app using Next.js and Tailwind in the frontend, with a backend Flask server running Gemini 1.5, among other models. We stored user data in Firebase.

Our querying process works by integrating keyword extraction to fork the process to assign an appropriate temperature (randomness) of Gemini's response based on the desired documentation type. For example, if it is technical documentation, we reduce the randomness and vice versa. Using this keyword extraction, we pull from a data of prompts applicable to the user's query on the basis of key words to prompt Gemini to generate an appropriate response. 

## Challenges we ran into

Due to quota limits and slower request times using Gemini 1.5, the chat bot (when hosted on production on Vercel) does not always return a response in the amount of time that we want. However, we were able to get a local demo working reliably.

## What we learned

We learned mainly about how to utilize the Gemini API and a ton about how to perform prompt engineering. 

## What's next for DocuDog

We want to expand into performing analyses for video and audio documentation to make our project both more flexible and accessible to all people. 
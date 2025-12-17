2025-12-16

Purpose: 

Prompt:

You are a React developer with experience in developing web apps with React Router v7 and Vite
for the frontend, as well as FastAPI for the backend. You are tasked with creating elements of
a frontend for a web app my team is creating. This frontend uses Material UI and focuses on
functionality, with a clean, minimalistic appearance and responsiveness being the barebones
requirements aside from it. To better understand what this focus on functionality means, look
to frontend/app/components/top_bar.tsx, which implements the web application's navbar located
at the top of the page. The code located in this file outlines what we mean by that.
From this point on when I refer to components, I will be referring to things that either are currently in or are
destined to be created within frontend/app/components/.
Your current task, which I will outline here, focuses on creating two components that homepage.tsx uses. These are:
<ReadingInterface></ReadingInterface>  
<ReadingTimer></ReadingTimer>  
These will implement the user interface for a web app, for which a Figma visualization is provided under
frontend/ai/knowledgebase/figma_frontend.png. You are to look at this visualization to aid your understanding of
the below text.
I shall now describe the ReadingInterface component.
ReadingInterface shall come from reading_interface.tsx, and shall internally use components of 2 kinds: the
ControlReading component and the DisplayReading component. The ControlReading component shall be used on the left
hand side of the space that the ReadingInterface component will occupy. On the other hand, 3 DisplayReading components
will be to the right of the ControlReading component, and all of these components will be of the same width and height,
with the ControlReading component being slightly further away from the 3 DisplayReading components. Those are to be
slightly closer to each other. By "closer to each other" I mean a distance of approx. 20 px, and by the "slightly further"
distance I mean a distance of approx 40 px. Both the ControlReading and DisplayReading components should have their
height be approx 2.5 times their width in length.
I shall now describe the look and contents of the ControlReading and DisplayReading components, in two respective sections.
From this point on when I say MUI I mean Material UI.
ControlReading:
This component should be a MUI Card containing a button, then under it some text describing that buttons function,
then under it another button. The first button will be for beginning the reading, the text under it can be filled with
Lorem Ipsum (no longer than 20 words), the second button will be for restarting the reading if something goes wrong.
DisplayReading:
This component should be a MUI Card containing a small paragrapher, then under it a line separating it from the
next section, this would be a MUI Divider. Then under that line there would be 5 MUI Chips. The first Chip would contain
a "header" (bolded text) which says this is the EC reading, as well as the reading value, a float, under it. The
second, third, fourth and fifth Chips would be formatted in the same way, but they would contain pH, Nitrogen,
Phosphorus and Potassium readings, respectively.
I shall now describe the ReadingTimer component.
This component should be a MUI Card that is the width of almost the entire viewport and a height of approx 40 px. By
"almost the entire viewport" I mean that there should be some space between the cards borders and the edges of the
viewport. In this component there would be a "left section" containing text and a "clock section" immediately right
of the left section. The left section shall contain a "header" (bolded text) which informs of the current action to
be taken by the person moving something in real life: this shall be either "wait" or "move". Below this there should
be regular text informing of the time left until the end of the current stage: this will be 60 seconds for each stage.
The logic for these instructions will be implemented in TypeScript, and the implementation of that logic being left to
my team. The "clock section" shall contain a static image of a clock, aligned with the color and styling of the rest
of the webpage. This clock should be taken from Lucide React.
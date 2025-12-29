Prompt #3:
There is a flaw in the current implementation of the stages of reading from the sensor. It should proceed as follows:
<Prompt #2 contents>
It currently works such that it does not leave the sensor for 60 seconds, but instead instantly switches to
commanding the user to move the sensor to the next pot.
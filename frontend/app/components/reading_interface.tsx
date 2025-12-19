import React, { useEffect, useState } from 'react';
import { Card, Button, Typography, Divider, Chip, Box } from '@mui/material';
import ReadingTimer from './reading_timer';

// MTP<N> -> move to pot N, LSB -> let sensor be
// MTP1, LSB, MTP2, LSB, MTP3, LSB
const TOTAL_STAGES = 6;
const STAGE_DURATION = 30; // seconds per stage

export default function ReadingInterface() {
  const [running, setRunning] = useState(false);
  const [stageIndex, setStageIndex] = useState(0);
  const [seconds, setSeconds] = useState(STAGE_DURATION);
  const [completed, setCompleted] = useState(false);
  const [accepted, setAccepted] = useState(false);

  // Using a timeout-driven effect to decrement the seconds counter and
  // to advance the stage exactly once when the timer reaches zero.
  useEffect(() => {
    if (!running) return undefined;

    // If we still have time left in the current stage, schedule a decrement
    if (seconds > 0) {
      const t = setTimeout(() => setSeconds(s => s - 1), 1000);
      return () => clearTimeout(t);
    }

    // seconds === 0 -> advance stage exactly once
    setStageIndex(si => {
      if (si < TOTAL_STAGES - 1) {
        // move to next stage and reset timer
        setSeconds(STAGE_DURATION);
        return si + 1;
      }

      // finished all stages
      setRunning(false);
      setCompleted(true);
      // keep seconds at 0 so UI can show completion if needed
      return si;
    });

    // no cleanup necessary here because advancing stage resets seconds or stops running
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [running, seconds]);

  function startReading() {
    setAccepted(false);
    setCompleted(false);
    setStageIndex(0);
    setSeconds(STAGE_DURATION);
    setRunning(true);
  }

  function abortReading() {
    setRunning(false);
    setAccepted(false);
    setCompleted(false);
    setStageIndex(0);
    setSeconds(STAGE_DURATION);
  }

  function acceptReading() {
    setAccepted(true);
    setCompleted(false);
    // leave readings in place or reset depending on UX
  }

  // Derive display text for current stage
  const actionText = (() => {
    if (stageIndex % 2 === 0) {
      // even indices are MTP stages: 0 -> pot1, 2 -> pot2, 4 -> pot3
      const pot = Math.floor(stageIndex / 2) + 1;
      return `Move the sensor to Pot ${pot}`;
    } else {
      return 'Reading in progress, do not move the sensor!';
    }
  })();

  // Simple ControlReading using parent handlers
  function ControlReading() {
    return (
      <Card style={{ height: '350px', width: '280px', display: 'flex', flexDirection: 'column', justifyContent: 'start', padding: '10px', gap: '20px' }}>
        <Typography variant="body2" style={{ textAlign: 'justify' }}>
            You will have 60 s to move the sensor to the first pot, and then it shall be left there for another 60 s.
            This will be repeated for pots 2 and 3. After that you either accept or reject.
        </Typography>
        <Button variant="contained" onClick={startReading} disabled={running}>Start Reading</Button>
        <Button variant="contained" color="error" onClick={abortReading}>Abort Reading</Button>

        {completed && !accepted && (
          <Button variant="contained" color="success" onClick={acceptReading} style={{ marginTop: 8 }}>
            Accept Reading
          </Button>
        )}
      </Card>
    );
  }

  function DisplayReading() {
    return (
      <Card style={{ height: '350px', width: '200px', padding: '10px', display: 'flex', flexDirection: 'column' }}>
        <Typography variant="body2">Reading Details</Typography>
        <Divider style={{ margin: '10px 0' }} />
        <Box style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
          <Chip label={<><b>EC:</b> 0.0</>} />
          <Chip label={<><b>pH:</b> 0.0</>} />
          <Chip label={<><b>Nitrogen:</b> 0.0</>} />
          <Chip label={<><b>Phosphorus:</b> 0.0</>} />
          <Chip label={<><b>Potassium:</b> 0.0</>} />
        </Box>
      </Card>
    );
  }

  return (
    <Box style={{ display: 'flex', flexDirection: 'column', gap: 20, padding: '20px' }}>
      <Box style={{ display: 'flex', justifyContent: 'center' }}>
        <Box style={{ display: 'flex', gap: 20 }}>
          <ControlReading />
          <DisplayReading />
          <DisplayReading />
          <DisplayReading />
        </Box>
      </Box>

      <ReadingTimer actionText={accepted ? 'Reading accepted' : actionText} seconds={running ? seconds : (completed ? 0 : seconds)} />
    </Box>
  );
}
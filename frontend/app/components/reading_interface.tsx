import React, { useEffect, useState } from 'react';
import { Card, Button, Typography, Divider, Chip, Box } from '@mui/material';
import ReadingTimer from './reading_timer';

// MTP<N> -> move to pot N, LSB -> let sensor be
// MTP1, LSB, MTP2, LSB, MTP3, LSB
const TOTAL_STAGES = 6;

export default function ReadingInterface() {
  const [running, setRunning] = useState(false);
  const [stageIndex, setStageIndex] = useState(0);
  const [seconds, setSeconds] = useState(60);
  const [completed, setCompleted] = useState(false);
  const [accepted, setAccepted] = useState(false);

  useEffect(() => {
    if (!running) return undefined;
    const id = setInterval(() => {
      setSeconds(prev => {
        if (prev > 1) return prev - 1;
        // time expired for current stage
        setStageIndex(si => {
          if (si < TOTAL_STAGES - 1) {
            return si + 1;
          } else {
            // finished all stages
            setRunning(false);
            setCompleted(true);
            return si;
          }
        });
        return 60;
      });
    }, 1000);
    return () => clearInterval(id);
  }, [running]);

  function startReading() {
    setAccepted(false);
    setCompleted(false);
    setStageIndex(0);
    setSeconds(60);
    setRunning(true);
  }

  function restartReading() {
    setRunning(false);
    setAccepted(false);
    setCompleted(false);
    setStageIndex(0);
    setSeconds(60);
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
      return `Move the sensor to pot ${pot}`;
    } else {
      return 'Reading in progress, do not move the sensor';
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
        <Button variant="contained" onClick={restartReading}>Restart Reading</Button>

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
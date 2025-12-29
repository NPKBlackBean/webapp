import React from 'react';
import { Card, Typography, Box } from '@mui/material';
import { Clock } from 'lucide-react';

type Props = {
  actionText: string;
  seconds: number;
};

export default function ReadingTimer({ actionText, seconds }: Props) {
  return (
    <Card style={{ width: 'calc(100vw - 40px)', maxWidth: '940px', height: '40px', margin: '0 auto', display: 'flex', alignItems: 'center', padding: '0 10px' }}>
      <Box style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <Typography variant="body1" style={{ fontWeight: 'bold' }}>{actionText}</Typography>
        <Typography variant="body2">Time left: {seconds} seconds</Typography>
      </Box>
      <Box style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <Clock size={20} />
      </Box>
    </Card>
  );
}
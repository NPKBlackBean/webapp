import React, { useEffect, useState } from 'react';
import { Card, Button, Typography, Divider, Chip, Box } from '@mui/material';
import ReadingTimer from './reading_timer';

const config = {
    units: {
        ec: import.meta.env.VITE_EC_UNIT,
        temperature: import.meta.env.VITE_TEMPERATURE_UNIT,
        humidity: import.meta.env.VITE_HUMIDITY_UNIT,
        nitrogen: import.meta.env.VITE_NITROGEN_UNIT,
        phosphorus: import.meta.env.VITE_PHOSPHORUS_UNIT,
        potassium: import.meta.env.VITE_POTASSIUM_UNIT,
    }
}

const TOTAL_STAGES = 6;
const STAGE_DURATION = 10;

interface SensorReading {
    EC: number;
    pH: number;
    N: number;
    P: number;
    K: number;
}

async function fetchSensorReading(): Promise<SensorReading> {
    const response = await fetch("http://localhost:8000/sensor_reading");
    return response.json();
}

async function putSensorReadings(readings: (SensorReading | null)[]): Promise<SensorReading> {
    const response = await fetch("http://localhost:8000/accepted_readings", {
        method: "POST",
        body: JSON.stringify({ readings: readings }),
        headers: {
            "Content-Type": "application/json"
        },
    });
    return response.json();
}

export default function ReadingInterface() {
    const [running, setRunning] = useState(false);
    const [stageIndex, setStageIndex] = useState(0);
    const [seconds, setSeconds] = useState(STAGE_DURATION);
    const [completed, setCompleted] = useState(false);
    const [accepted, setAccepted] = useState(false);
    const [readings, setReadings] = useState<(SensorReading | null)[]>([null, null, null]);

    // Timer effect (unchanged)
    useEffect(() => {
        if (!running) return undefined;

        if (seconds > 0) {
            const t = setTimeout(() => setSeconds(s => s - 1), 1000);
            return () => clearTimeout(t);
        }

        setStageIndex(si => {
            if (si < TOTAL_STAGES - 1) {
                setSeconds(STAGE_DURATION);
                return si + 1;
            }
            setRunning(false);
            setCompleted(true);
            return si;
        });
    }, [running, seconds]);

    // Fetch when entering a reading stage (odd indices: 1, 3, 5)
    useEffect(() => {
        if (!running) return;
        if (stageIndex % 2 !== 1) return;

        const readingIdx = Math.floor(stageIndex / 2);

        fetchSensorReading()
            .then(data => {
                setReadings(prev => {
                    const next = [...prev];
                    next[readingIdx] = data;
                    return next;
                });
            })
            .catch(err => console.error('Sensor fetch failed:', err));
    }, [running, stageIndex]);

    function startReading() {
        setAccepted(false);
        setCompleted(false);
        setStageIndex(0);
        setSeconds(STAGE_DURATION);
        setReadings([null, null, null]);
        setRunning(true);
    }

    function abortReading() {
        setRunning(false);
        setAccepted(false);
        setCompleted(false);
        setStageIndex(0);
        setSeconds(STAGE_DURATION);
    }

    function acceptReading(readings: (SensorReading | null)[]) {
        setAccepted(true);
        setCompleted(false);
        putSensorReadings(readings).then((json) => console.log(json));
    }

    const actionText = (() => {
        if (stageIndex % 2 === 0) {
            const pot = Math.floor(stageIndex / 2) + 1;
            return `Move the sensor to Pot ${pot}`;
        }
        return 'Reading in progress, do not move the sensor!';
    })();

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
                    <Button variant="contained" color="success" onClick={() => acceptReading(readings)} style={{ marginTop: 8 }}>
                        Accept Reading
                    </Button>
                )}
            </Card>
        );
    }

    function DisplayReading({ potNumber, reading, showData }: { potNumber: number; reading: SensorReading | null; showData: boolean }) {
        const display = showData && reading ? reading : { EC: 0.0, pH: 0.0, N: 0.0, P: 0.0, K: 0.0 };

        return (
            <Card style={{ height: '350px', width: '200px', padding: '10px', display: 'flex', flexDirection: 'column' }}>
                <Typography variant="body2">Pot {potNumber}</Typography>
                <Divider style={{ margin: '10px 0' }} />
                <Box style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start', gap: 6 }}>
                    <Chip label={<><b>EC:</b> {display.EC} {config.units.ec}</>} />
                    <Chip label={<><b>pH:</b> {display.pH}</>} />
                    <Chip label={<><b>Nitrogen:</b> {display.N} {config.units.nitrogen}</>} />
                    <Chip label={<><b>Phosphorus:</b> {display.P} {config.units.phosphorus}</>} />
                    <Chip label={<><b>Potassium:</b> {display.K} {config.units.potassium}</>} />
                </Box>
            </Card>
        );
    }

    const showData = completed || accepted;

    return (
        <Box style={{ display: 'flex', flexDirection: 'column', gap: 20, padding: '20px' }}>
            <Box style={{ display: 'flex', justifyContent: 'center' }}>
                <Box style={{ display: 'flex', gap: 20 }}>
                    <ControlReading />
                    <DisplayReading potNumber={1} reading={readings[0]} showData={showData} />
                    <DisplayReading potNumber={2} reading={readings[1]} showData={showData} />
                    <DisplayReading potNumber={3} reading={readings[2]} showData={showData} />
                </Box>
            </Box>
            <ReadingTimer actionText={accepted ? 'Reading accepted' : actionText} seconds={running ? seconds : (completed ? 0 : seconds)} />
        </Box>
    );
}
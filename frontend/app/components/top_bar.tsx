import { useQuery } from '@tanstack/react-query'
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
// @ts-ignore
import MenuIcon from '@mui/icons-material/Menu';

async function fetchBackendIP() {
    const response = await fetch("http://localhost:8000/backend_ip")
    return response.json()
}

export default function ButtonAppBar() {
    const { data, isLoading, error } = useQuery({
        queryKey: ['backend-ip'],
        queryFn: fetchBackendIP
    })

    if (isLoading) return <div>Loading...</div>
    if (error) return <div>Error loading IP</div>

    return (
        <Box sx={{ flexGrow: 1 }}>
            <AppBar position="static">
                <Toolbar>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                        You are connected to RPi@{data.ip_address}
                    </Typography>
                </Toolbar>
            </AppBar>
        </Box>
    );
}

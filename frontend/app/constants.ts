let rpi_ip_address: string = import.meta.env.RPI_IP;
let backend_port: string = import.meta.env.FASTAPI_PORT;

export {rpi_ip_address, backend_port}
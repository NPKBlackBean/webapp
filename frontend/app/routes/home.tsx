import {
    useQuery,
    useMutation,
    useQueryClient,
    QueryClient,
    QueryClientProvider,
} from '@tanstack/react-query'
import type { Route } from "./+types/home";
import Homepage from "../components/homepage";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Sensor Data Collection App" },
    { name: "description", content: "An application to collect and analyze sensor data for soil quality monitoring." },
  ];
}

const queryClient = new QueryClient()

export default function Home() {
  return (
      <QueryClientProvider client={queryClient}>
        <Homepage />
      </QueryClientProvider>
  );
}

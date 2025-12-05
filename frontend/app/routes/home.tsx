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
    { title: "New React Router App" },
    { name: "description", content: "Welcome to React Router!" },
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

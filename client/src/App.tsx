import { useEffect } from 'react';
import UserList from "@/components/UserList";
import StatusComponent from "@/components/StatusComponent";

function App() {
  useEffect(() => {
    console.log('App component mounted');
    document.title = 'My Boilerplate App - Loaded';
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-svh p-6">
      <header className="App-header mb-8 text-center">
        <h1 className="text-3xl font-bold mb-4">Welcome to My Boilerplate App</h1>
        <p className="text-lg mb-6">This is a basic setup using FastAPI for the backend and Vite+React for the frontend.</p>
        <StatusComponent />
      </header>
      
      <main className="w-full max-w-2xl">
        <UserList />
      </main>
    </div>
  );
}

export default App;
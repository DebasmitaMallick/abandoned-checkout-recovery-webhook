import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import './App.css';
import Home, { loader } from './pages/Home';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Home />,
    loader: loader
  }
])

function App() {
  return <RouterProvider router={router} />
}

export default App;

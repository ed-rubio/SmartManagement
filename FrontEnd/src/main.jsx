import './CSS/index.css'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { Children, StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import Home from './routes/pages/Home.jsx'
import EoqPage from './routes/pages/EoqPage.jsx'
import NotFound from './routes/NotFound/NotFound.jsx'
import App from './App.jsx'

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      {
        path: '/home',
        element: <Home />
      },
      {
        path: '/eogpage',
        element: <EoqPage />
      }
    ]
  },
  {
    path: '*',
    element: <NotFound />
  },
])

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
)

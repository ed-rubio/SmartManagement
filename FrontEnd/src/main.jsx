import './CSS/index.css'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { StrictMode, lazy } from 'react'
import { createRoot } from 'react-dom/client'

// Imports for routes
import Home from './routes/pages/Home.jsx'
import EoqPage from './routes/pages/EoqPage.jsx'
import NotFound from './routes/NotFound/NotFound.jsx'

const App  = lazy(() => import('./App.jsx'))

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      {
        path: '/',
        element: <Home />
      },
      {
        path: '/Eoqpage',
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

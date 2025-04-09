import { StrictMode, lazy } from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import './CSS/index.css'
import Home from './routes/pages/Home.jsx'
import EoqPage from './routes/pages/EoqPage.jsx'
import NotFound from './routes/NotFound/NotFound.jsx'
import Formulario from './routes/pages/Formulario.jsx'

const App = lazy(() => import('./App.jsx'))

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      {
        path: '/',
        element: <Home />,
      },
      {
        path: '/eoqpage',
        element: <EoqPage />
      },
      {
        path: '*',
        element: <NotFound />
      },
      {
        path: '/login',
        element: <Formulario />
      }
      

    ]
  }


])

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)

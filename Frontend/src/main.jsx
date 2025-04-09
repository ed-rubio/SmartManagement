import { StrictMode, lazy } from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import './CSS/index.css'
import Home from './routes/pages/Home.jsx'
import NotFound from './routes/NotFound/NotFound.jsx'
// import Formulario from './routes/pages/Formulario.jsx'
import MathScreen from './routes/pages/MathScreen.jsx'
import HowTo from './routes/pages/HowTo.jsx'


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
        path: '/math',
        element: <MathScreen />
      },
      {
        path: '*',
        element: <NotFound />
      },
      {
        path: '/instrucciones',
        element: <HowTo />
      }
      // {
      //   path: '/login',
      //   element: <Formulario />
      // }
    ]
  }
])

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)

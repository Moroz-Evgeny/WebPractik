import { BrowserRouter, Routes, Route } from 'react-router-dom'

import LogForm from './components/pages/LogForm'
import RegForm from './components/pages/RegForm'
import ProfilePage from './components/pages/ProfilePage'

function App() {
	return (
		<div className='App'>
			<LogForm />
		</div>
	)
}

export default App

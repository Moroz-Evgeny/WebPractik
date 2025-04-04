import React, { useEffect, useState } from 'react'

export default function ProfilePage() {
	const [userData, setUserData] = useState({})
	function decodeJWT(token) {
		const base64Url = token.split('.')[1]
		const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
		return JSON.parse(atob(base64))
	}

	const handleSubmit = async () => {
		// event.preventDefault()

		const token = localStorage.getItem('token')
		const data = decodeJWT(token)

		fetch(`http://37.9.4.131:8000/user/?id=${data.sub}`, {
			method: 'GET',
			headers: {
				Authorization: `Bearer ${token}`,
				'Content-Type': 'application/json',
			},
		})
			.then(response => response.json())
			.then(result => {
				setUserData(result)
				console.log(result)
			})
			.catch(error => console.error('Ошибка запроса:', error))
	}

	useEffect(() => {
		handleSubmit()
	}, [])

	return (
		<div>
			<div className='profile-box'>
				<h4>Личный кабинет</h4>
				<p>{userData.name}</p>
				<p>{userData.role}</p>
			</div>
		</div>
	)
}

import React, { useEffect, useState } from 'react'

export default function LogForm() {
	const [emailForm, setEmailForm] = useState('')
	const [passwordForm, setPasswordForm] = useState('')
	const [token, setToken] = useState(localStorage.getItem('token') || '')
	const [btnStyle, setBtnStyle] = useState('btn disable')
	const [data, setData] = useState({})

	useEffect(() => {
		if (emailForm === '' || passwordForm === '') {
			setBtnStyle('btn disable')
		} else {
			setBtnStyle('btn')
		}
	}, [emailForm, passwordForm])

	function handleEmailInput(e) {
		setEmailForm(e.target.value)
	}
	function handlePasswordInput(e) {
		setPasswordForm(e.target.value)
	}

	const handleSubmit = event => {
		event.preventDefault()
		const formData = {
			email: emailForm,
			password: passwordForm,
		}

		fetch('http://127.0.0.1:8000/user', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(formData),
		})
			.then(response => response.json())
			.then(result => {
				if (result.token) {
					localStorage.setItem('token', result.token)
					setToken(result.token)
				}
				setData(result)
			})
			.catch(error => console.error('Ошибка запроса:', error))
	}

	return (
		<form className='register_form' onSubmit={handleSubmit}>
			<div className='form_input'>
				<label htmlFor='input'>Почта</label>
				<input type='text' onChange={handleEmailInput} value={emailForm} />
			</div>
			<div className='form_input'>
				<label htmlFor='input'>Пароль</label>
				<input
					type='password'
					onChange={handlePasswordInput}
					value={passwordForm}
				/>
			</div>

			<button type='submit' className={btnStyle}>
				Войти
			</button>
		</form>
	)
}

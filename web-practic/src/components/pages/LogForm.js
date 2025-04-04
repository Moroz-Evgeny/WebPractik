import React, { useEffect, useState } from 'react'




export default function LogForm() {
	const [emailForm, setEmailForm] = useState('')
	const [passwordForm, setPasswordForm] = useState('')
	const [token, setToken] = useState(localStorage.getItem('token') || '')
	const [btnStyle, setBtnStyle] = useState('btn disable')
	const [data, setData] = useState({})

	const [isEmailValid, setIsEmailValid] = useState(true)

	var email = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/

	useEffect(() => {
		if (emailForm === '' || passwordForm === '') {
			setBtnStyle('btn disable')
		} else {
			setBtnStyle('btn')
		}

		if (!email.test(emailForm) && emailForm !== '') {
			setIsEmailValid(false)
			setBtnStyle('btn disable')
		} else if (emailForm !== '' || emailForm === '') {
			setIsEmailValid(true)
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
			grant_type: 'password',
			username: emailForm,
			password: passwordForm,
			scope: '',
			client_id: '',
			client_secret: '',
		}

		fetch('http://37.9.4.131:8000/login', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded',
			},
			body: new URLSearchParams(formData).toString(),
		})
			.then(response => response.json())
			.then(result => {
				if (result.access_token) {
					localStorage.setItem('token', result.access_token)
					setToken(result.access_token)
				}
				setData(result)
			})
			.catch(error => console.error('Ошибка запроса:', error))
	}		
	
	return (
		<form className='register_form' onSubmit={handleSubmit}>
			<div className='form_input'>
				<label htmlFor='input'>Почта</label>
				<div className='input'>
					<input
						type='text'
						onChange={handleEmailInput}
						value={emailForm}
						placeholder='example@example.ru'
					/>
					<label className='label' htmlFor='input'>
						{isEmailValid ? '' : 'Почта введена некорректно'}
					</label>
				</div>
			</div>
			<div className='form_input'>
				<label htmlFor='input'>Пароль</label>
				<input
					type='password'
					onChange={handlePasswordInput}
					value={passwordForm}
					placeholder='Пароль'
				/>
			</div>

			<button type='submit' className={btnStyle}>
				Войти
			</button>
		</form>
	)
}

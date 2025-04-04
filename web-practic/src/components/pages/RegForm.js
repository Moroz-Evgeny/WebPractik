import React, { useEffect, useState } from 'react'

export default function RegForm() {
	var email = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
	const [nameForm, setNameForm] = useState('')
	const [surnameForm, setSurnameForm] = useState('')
	const [emailForm, setEmailForm] = useState('')
	const [passwordForm, setPasswordForm] = useState('')
	const [radioForm, setRadioForm] = useState({
		TeamLead: 'ROLE_PORTAL_TEAMLID',
		TeamMate: 'ROLE_PORTAL_USER',
	})
	const [rank, setRank] = useState('')
	const [btnStyle, setBtnStyle] = useState('btn disable')
	const [data, setData] = useState({})
	const [isNameValid, setIsNameValid] = useState(true)
	const [isSurnameValid, setIsSurnameValid] = useState(true)
	const [isEmailValid, setIsEmailValid] = useState(true)

	useEffect(() => {
		if (
			nameForm === '' ||
			!/^[A-Za-z]+$/.test(nameForm) ||
			surnameForm === '' ||
			!/^[A-Za-z]+$/.test(surnameForm) ||
			emailForm === '' ||
			passwordForm === '' ||
			rank === ''
		) {
			setBtnStyle('btn disable')
		} else {
			setBtnStyle('btn')
		}
		if (/\d/.test(nameForm)) {
			setIsNameValid(false)
			setBtnStyle('btn disable')
		} else {
			setIsNameValid(true)
		}

		if (/\d/.test(surnameForm)) {
			setIsSurnameValid(false)
			setBtnStyle('btn disable')
		} else {
			setIsSurnameValid(true)
		}

		if (!email.test(emailForm) && emailForm !== '') {
			setIsEmailValid(false)
			setBtnStyle('btn disable')
		} else if (emailForm !== '' || emailForm === '') {
			setIsEmailValid(true)
		}

	}, [nameForm, surnameForm, emailForm, passwordForm, rank])

	function handleNameInput(e) {
		setNameForm(e.target.value)
	}
	function handleSurNameInput(e) {
		setSurnameForm(e.target.value)
	}
	function handleEmailInput(e) {
		setEmailForm(e.target.value)
	}
	function handlePasswordInput(e) {
		setPasswordForm(e.target.value)
	}
	function handleRadioInput(e) {
		if (e.target.id === radioForm.TeamLead) {
			setRank(radioForm.TeamLead)
		} else {
			setRank(radioForm.TeamMate)
		}
	}

	const handleSubmit = event => {
		event.preventDefault()
		const formData = {
			name: nameForm,
			surname: surnameForm,
			email: emailForm,
			password: passwordForm,
			role: rank,
		}

		fetch('http://37.9.4.131:8000/user', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(formData),
		})
			.then(response => response.json())
			.then(result => {
				console.log(result)
				setData(result)
			})
			.catch(error => console.error('Ошибка запроса:', error))
	}

	return (
		<form className='register_form' onSubmit={handleSubmit}>
			<div className='form_input'>
				<label htmlFor='input'>Имя</label>
				<div className='input'>
					<input
						type='text'
						onChange={handleNameInput}
						value={nameForm}
						placeholder='Введите имя'
					/>
					<label className='label' htmlFor='input'>
						{isNameValid ? '' : 'Имя введено некорректно'}
					</label>
				</div>
			</div>
			<div className='form_input'>
				<label htmlFor='input'>Фамилия</label>
				<div className='input'>
					<input
						type='text'
						onChange={handleSurNameInput}
						value={surnameForm}
						placeholder='Введите фамилию'
					/>
					<label className='label' htmlFor='input'>
						{isSurnameValid ? '' : 'Фамилия введена некорректно'}
					</label>
				</div>
			</div>
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
					type='text'
					onChange={handlePasswordInput}
					value={passwordForm}
					placeholder='Введите пароль'
				/>
			</div>
			<div>
				<label htmlFor='radio'>TeamLead</label>
				<input
					className='radio'
					name='rank'
					type='radio'
					onChange={handleRadioInput}
					id={radioForm.TeamLead}
					value={radioForm.TeamLead}
				/>
				<label htmlFor='radio'>TeamMate</label>
				<input
					className='radio'
					name='rank'
					type='radio'
					onChange={handleRadioInput}
					id={radioForm.TeamMate}
					value={radioForm.TeamMate}
				/>
			</div>
			<button type='submit' className={btnStyle}>
				Зарегистрироваться
			</button>
		</form>
	)
}

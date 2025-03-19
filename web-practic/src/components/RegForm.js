import React, { useState } from 'react'

export default function RegForm() {

    const [nameForm, setNameForm] = useState("")
    const [surnameForm, setSurnameForm] = useState("")
    const [emailForm, setEmailForm] = useState("")
    const [passwordForm, setPasswordForm] = useState("")
    const [radioForm, setRadioForm] = useState({TeamLead : "ROLE_PORTAL_TEAMLID",
        TeamMate : "ROLE_PORTAL_USER"
    })
    const [rank, setRank] = useState("") 
    const [btnStyle, setBtnStyle] = useState("btn disable")
    const [data, setData] = useState({});

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
        }
        else {
            setRank(radioForm.TeamMate)
        }        
    }

    const handleSubmit = (event) => {
        event.preventDefault();
        const formData = {name : nameForm,
            surname : surnameForm,
            email : emailForm,
            password : passwordForm,
            rank : rank
        };

        fetch('http://127.0.0.1:8000/user', {
            
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
    };

  return (
    <form className='register_form' onSubmit={handleSubmit}>        
        <div className='form_input'>
            <label htmlFor="input">Имя</label>
            <input type="text" onChange={handleNameInput} value={nameForm}/>
        </div>
        <div className='form_input'>
            <label htmlFor="input">Фамилия</label>
            <input type="text" onChange={handleSurNameInput} value={surnameForm}/>
        </div>
        <div className='form_input'>
            <label htmlFor="input">Почта</label>
            <input type="text" onChange={handleEmailInput} value={emailForm}/>
        </div>
        <div className='form_input'>
            <label htmlFor="input">Пароль</label>
            <input type="text" onChange={handlePasswordInput} value={passwordForm}/>
        </div>
        <div>  
            <label htmlFor="radio" >TeamLead</label>
            <input className='radio' name="rank" type="radio" onChange={handleRadioInput} id={radioForm.TeamLead} value={radioForm.TeamLead} />    
            <label htmlFor="radio">TeamMate</label>    
            <input className='radio' name='rank' type="radio" onChange={handleRadioInput} id={radioForm.TeamMate} value={radioForm.TeamMate}/>
        </div>
        <button type='submit' className={btnStyle}>Зарегистрироваться</button>
       
    </form>
  )
}

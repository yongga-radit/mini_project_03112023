import React, {useState, useEffect} from 'react'
import api from './App.css'

const App = () => {
  const [users, setUsers] = useState([]);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirm_password: ''
  });
  const fetchUsers = async() => {
    const response = await api.get('/user/sign-up')
    setUsers(response.data)
  };
  
  useEffect(() => {
    fetchUsers();
  }, []);

  const handleInputChange = (event) => {
    const value = event.target.type == 'checkbox' ? event.target.checked: event.target.value;
    setFormData({
      ...formData,
      [event.target.name]: value,
    });
  };

  const handelFormSubmit = async (event) => {
    event.preventDefault();
    await api.post('/user/sign-up', formData);
    fetchUsers();
    setFormData({
      name: '',
      email: '',
      password: '',
      confirm_password: ''
    })
  };



  return (
    <div>

      <nav className='navba navbar-dark bg-primary'>
        <div className='container-fluid'>
          <a className='navbar-brand' href="#">
            Mini Project 27112023
          </a>
        </div>
      </nav>
      
      <div className='container'>
        <form onSubmit={handelFormSubmit}>

          <div className='mb-3 mt-3'>
            <label htmlFor='name' className='form-label'>
              Name
            </label>
            <input type='text' className='form-control' id='name' name='name' onChange={handleInputChange} value={formData.name}/>
          </div>

          <div className='mb-3'>
            <label htmlFor='email' className='form-label'>
              E-mail
            </label>
            <input type='text' className='form-control' id='email' name='email' onChange={handleInputChange} value={formData.email}/>
          </div>

          <div className='mb-3'>
            <label htmlFor='password' className='form-label'>
              Password
            </label>
            <input type='password' className='form-control' id='password' name='password' onChange={handleInputChange} value={formData.password}/>
          </div>

          <div className='mb-3'>
            <label htmlFor='confirm_password' className='form-label'>
              Confirm Password
            </label>
            <input type='password' className='form-control' id='confirm_password' name='confirm_password' onChange={handleInputChange} value={formData.confirm_password}/>
          </div>

          <button type='submit' className='btn btn-primary'>
            Create
          </button>
        </form>
      </div>

    </div>
  )
}



export default App;

// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;

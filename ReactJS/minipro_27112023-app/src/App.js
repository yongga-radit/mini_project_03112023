import React, {useState, useEffect} from 'react'
import api from './api'

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
  }

  return (
    <div>
      <nav className='navba navbar-dark bg-primary'>
        <div className='container-fluid'>
          <a className='navbar-brand' href="#">
            Mini Project 27112023
          </a>
        </div>
      </nav>
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
